document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('issueForm');
    const progress = document.getElementById('progress');

    let web3;
    if (typeof window.ethereum !== 'undefined') {
        web3 = new Web3(Web3.givenProvider || CONFIG.RPC_URL);
        window.ethereum.request({ method: 'eth_requestAccounts' }).catch(() => alert('Please allow access to your accounts.'));
    } else {
        alert('MetaMask not detected. Please install MetaMask to use this feature.');
    }
    
    // Contract details
    const contractABI = CONFIG.CONTRACT_ABI
    const contractAddress = CONFIG.CONTRACT_ADDRESS;
    const contract = new web3.eth.Contract(contractABI, contractAddress);


    // Handle form submission
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = getFormData();
        const credentialHash = web3.utils.sha3(JSON.stringify(formData.credential));

        displayLoading(true);

        try {
            const account = await getAccountAddress();
            const ipfsHash = await uploadToPinata(formData.credential, account);

            const receipt = await issueCredential(contract, credentialHash, ipfsHash.IpfsHash, account);
            await saveCredentialToDB(formData, receipt.transactionHash, credentialHash);
            alert('Credential issued successfully!');
        } catch (error) {
            console.error(error);
            alert('Error issuing credential.');
        } finally {
            showProgress(false);
        }
    });

    async function getAccountAddress() {
        const accounts = await web3.eth.getAccounts();
        return accounts[0];
    }

    async function issueCredential(contract, credentialHash, ipfs_hash, account) {
        return contract.methods.issueCredential(credentialHash, ipfs_hash).send({ from: account });
    }

    async function uploadToPinata(credentialData, issuerAddress) {
        const response = await fetch('/upload_to_pinata/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ credential: credentialData, issuerAddress })
        });
    
        const data = await response.json();
        if (data.status !== 'success') throw new Error('Failed to upload to Pinata');
        
        return data.ipfs_hash;
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

    function displayLoading(show) {
        progress.classList.toggle('d-none', !show);
    }
    
});

