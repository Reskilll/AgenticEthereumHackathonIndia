const { ethers } = require('hardhat');

const main = async () => {
    try {
        // const Verifier = await ethers.getContractFactory('Verifier')
        const VerifierAge = await ethers.getContractFactory('./VerifierAge/Groth16Verifier');
        const VerifierLocation = await ethers.getContractFactory('./VerifierLocation/Groth16Verifier');
        const AgeVerifier = await ethers.getContractFactory('AgeVerifier');
        const LocationVerifier = await ethers.getContractFactory('LocationVerifier');

        console.log('Deploying verifier on Ethereum verifier...');

        const verifierAge = await VerifierAge.deploy();
        await verifierAge.deploymentTransaction().wait();

        const ageVerifier = await AgeVerifier.deploy(await verifierAge.getAddress());
        await ageVerifier.deploymentTransaction().wait();

        const verifierLocation = await VerifierLocation.deploy();
        await verifierLocation.deploymentTransaction().wait();

        const locationVerifier = await LocationVerifier.deploy(await verifierLocation.getAddress());
        await locationVerifier.deploymentTransaction().wait();

        console.log("Verifier for Age deployed at:", await verifierAge.getAddress());
        console.log("AgeVerifier deplo  yed at:", await ageVerifier.getAddress());
        console.log("Verifier for Location deployed at:", await verifierLocation.getAddress());
        console.log("LocationVerifier deployed at:", await locationVerifier.getAddress());
    } catch (error) {
        console.error(error);
        process.exit(1);

    }
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    })
