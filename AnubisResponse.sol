// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";

abstract contract AnubisResponse is AccessControl {
    bool public paused;
    address public immutable automationRouter;
    
    bytes32 public constant UNPAUSE_ROLE = keccak256("UNPAUSE_ROLE");

    event ContractPaused(address indexed by);
    event ContractUnpaused(address indexed by);

    constructor(address _automationRouter) {
        automationRouter = _automationRouter;
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    modifier whenNotPaused() {
        require(!paused, "Contract paused");
        _;
    }

    function pause() external {
        require(msg.sender == automationRouter, "Unauthorized pause");
        paused = true;
        emit ContractPaused(msg.sender);
    }

    function unpause() external onlyRole(UNPAUSE_ROLE) {
        paused = false;
        emit ContractUnpaused(msg.sender);
    }
}