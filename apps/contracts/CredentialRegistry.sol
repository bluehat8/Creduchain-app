// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CredentialRegistry {
    struct Credential {
        bytes32 credentialHash;
        address issuer;
        uint256 issuedAt;
    }

    mapping(bytes32 => Credential) public credentials;
    mapping(address => bool) public authorizedIssuers;

    event CredentialIssued(bytes32 indexed credentialHash, address indexed issuer, uint256 issuedAt);
    event AuthorizedIssuerAdded(address indexed issuer);
    event AuthorizedIssuerRemoved(address indexed issuer);

    address public owner;

    modifier onlyAuthorizedIssuer() {
        require(authorizedIssuers[msg.sender], "Not authorized issuer.");
        _;
    }

    constructor() {
        owner = msg.sender; // El creador del contrato se establece como el propietario
        authorizedIssuers[owner] = true; // El propietario es un emisor autorizado por defecto
    }

    function addAuthorizedIssuer(address _issuer) public {
        require(msg.sender == owner, "Only owner can add authorized issuers.");
        authorizedIssuers[_issuer] = true;
        emit AuthorizedIssuerAdded(_issuer);
    }

    // Función para revocar el acceso a emisores autorizados
    function revokeAuthorizedIssuer(address _issuer) public {
        require(msg.sender == owner, "Only owner can revoke authorized issuers.");
        require(authorizedIssuers[_issuer], "Issuer not authorized.");
        authorizedIssuers[_issuer] = false;
        emit AuthorizedIssuerRemoved(_issuer);
    }

    // Emitir credencial almacenando su hash en la blockchain
    function issueCredential(bytes32 _credentialHash) public onlyAuthorizedIssuer {
        require(credentials[_credentialHash].issuer == address(0), "Credential already exists.");

        credentials[_credentialHash] = Credential({
            credentialHash: _credentialHash,
            issuer: msg.sender,
            issuedAt: block.timestamp // Se va considerar usar block.number
        });

        emit CredentialIssued(_credentialHash, msg.sender, block.timestamp);
    }

    function verifyCredential(bytes32 _credentialHash) public view returns (bool) {
        return credentials[_credentialHash].issuer != address(0);
    }
}