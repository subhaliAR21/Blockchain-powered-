let Certification = artifacts.require("./Certification.sol");
const fs = require('fs');

module.exports = async function (deployer) {
  await deployer.deploy(Certification);
  const deployedCertification = await Certification.deployed();

  let configData = {};
  configData.Certification = deployedCertification.address;

  fs.writeFileSync('./deployment_config.json', JSON.stringify(configData, null, 2));

  console.log(`Certification contract deployed at address: ${deployedCertification.address}`);
}
