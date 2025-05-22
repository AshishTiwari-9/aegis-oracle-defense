// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

interface IAnubis {
    function pause() external;
}

contract AegisAutomation {
    address public ANUBIS;
    string public API_URL = "https://api.aegis.dev/alerts";
    
    constructor(address anubis) {
        ANUBIS = anubis;
    }

    function setAnubis(address anubis) external {
    require(ANUBIS == address(0), "Already set");
    ANUBIS = anubis;
    }

    function checkUpkeep(bytes calldata) 
        external view returns (bool upkeepNeeded, bytes memory performData) 
    {
        // Chainlink nodes verify API response consensus
        return (true, abi.encode(ANUBIS));
    }

    function performUpkeep(bytes calldata) external {
        IAnubis(ANUBIS).pause();
    }
}