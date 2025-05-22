// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Dummy price feed contract for testing
contract KiloPriceFeed {
    uint256 public ethPrice;
    uint256 public lastUpdate;

    // Vulnerable: anyone can call this and set any price
    function setPrices(uint256 _newPrice) public {
        ethPrice = _newPrice;
        lastUpdate = block.timestamp;
    }

    // Returns the latest price set
    function getLatestPrice() public view returns (uint256) {
        return ethPrice;
    }

    // Returns the last update timestamp
    function getLastUpdate() public view returns (uint256) {
        return lastUpdate;
    }
}
