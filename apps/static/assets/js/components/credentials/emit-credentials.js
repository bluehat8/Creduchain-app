document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('issueForm');
    const progress = document.getElementById('progress');

    // Initialize Web3
    let web3;
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(Web3.givenProvider || 'https://sepolia-rpc.scroll.io/');
        window.ethereum.request({ method: 'eth_requestAccounts' }).catch(() => alert('Please allow access to your accounts.'));
    } else {
        alert('MetaMask not detected. Please install MetaMask to use this feature.');
    }

    // Smart contract details
    const contractABI = [{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"credentialHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"issuer","type":"address"},{"indexed":false,"internalType":"uint256","name":"issuedAt","type":"uint256"}],"name":"CredentialIssued","type":"event"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"credentials","outputs":[{"internalType":"bytes32","name":"credentialHash","type":"bytes32"},{"internalType":"address","name":"issuer","type":"address"},{"internalType":"uint256","name":"issuedAt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_credentialHash","type":"bytes32"}],"name":"issueCredential","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_credentialHash","type":"bytes32"}],"name":"verifyCredential","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}];
    const contractAddress = '0x305d2f4172325e970C61206fD58323C93900670e';
    const contract = new web3.eth.Contract(contractABI, contractAddress);

    // Handle form submission
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = getFormData();
        const credentialHash = web3.utils.sha3(JSON.stringify(formData.credential));

        showProgress(true);

        try {
            const account = await getAccountAddress();
            const receipt = await issueCredential(contract, credentialHash, account);
            await saveCredentialToDB(formData, receipt.transactionHash, credentialHash);
            alert('Credential issued successfully!');
        } catch (error) {
            console.error(error);
            alert('Error issuing credential.');
        } finally {
            showProgress(false);
        }
    });

    function getFormData() {
        const name = document.getElementById('name').value;
        const studentId = document.getElementById('studentId').value;
        const program = document.getElementById('program').value;
        const graduationDate = document.getElementById('graduationDate').value;
        const credentialType = document.getElementById('credentialType').value;

        return {
            credential: {
                "@context": ["https://www.w3.org/2018/credentials/v1"],
                "type": ["VerifiableCredential", credentialType],
                "issuer": `did:ethr:${getAccountAddress()}`,
                "issuanceDate": new Date().toISOString(),
                "credentialSubject": {
                    "id": `did:example:student:${studentId}`,
                    "name": name,
                    "program": program,
                    "graduationDate": graduationDate,
                    "credentialType": credentialType
                }
            },
            issuerAddress: getAccountAddress(),
            studentId,
            name,
            program,
            graduationDate,
            credentialType,
        };
    }

    async function getAccountAddress() {
        const accounts = await web3.eth.getAccounts();
        return accounts[0];
    }

    async function issueCredential(contract, credentialHash, account) {
        return contract.methods.issueCredential(credentialHash).send({ from: account });
    }

    async function saveCredentialToDB(credentialData, transactionHash, credentialHash) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = await fetch('/emit-credentials/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ ...credentialData, credentialHash ,transactionHash })
        });
        const data = await response.json();
        if (data.status !== 'success') throw new Error('Database save failed');
        window.location.href = data.redirect;
    }

    function showProgress(show) {
        progress.classList.toggle('d-none', !show);
    }
    
});

