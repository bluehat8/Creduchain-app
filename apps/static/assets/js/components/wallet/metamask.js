document.getElementById('connect-wallet').addEventListener('click', async () => {
// Comprobar si el navegador tiene una wallet instalada
if (typeof window.ethereum !== 'undefined') {
    try {
    // Solicitar conexión a la wallet
    web3 = new Web3(Web3.givenProvider || 'https://sepolia-rpc.scroll.io/');
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
    const account = accounts[0];

    // Mostrar la dirección de la wallet conectada (puedes personalizar esto)
    alert(`Wallet conectada: ${account}`);
    } catch (error) {
    console.error("Error al conectar a la wallet:", error);
    alert('No se pudo conectar a la wallet. Asegúrate de que MetaMask esté instalado y habilitado.');
    }
} else {
    alert('Por favor, instala MetaMask u otra wallet compatible.');
}
});

