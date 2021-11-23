pragma solidity >=0.4.21 <0.7.0;

contract Registerations {
    mapping(address => bool) registered;
    address public owner;
    constructor() public {
        // owner = msg.sender;
    }
    function isRegistered(address user) public view returns (bool) {
        return registered[user];

    }
    // modifier onlyOwner() {
    //     require(msg.sender == owner, "Access denied");
    //     _;

    // }
    function register(address user) public {
        registered[user] = true;
    }

}
