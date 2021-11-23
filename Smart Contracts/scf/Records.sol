pragma solidity >=0.4.21 <0.7.0;

import "./SCFContracts.sol";
import "../token/Token.sol";

contract Records {
    mapping(bytes32 => SFCContracts) records;
    Token private token;
    Registerations private registerations;

    constructor() public {}

    modifier checkUser(address _address) {
        require(registerations.isRegistered(_address), "Access Denied");
        _;
    }

    function register(address _address) public {
        registerations.register(_address);
    }

    function createContract(bytes32 _id) public {
        records[_id] = (new SFCContracts(_id));

    }

    function setInitial(
        bytes32 _id,
        bytes32 _dateDelivery,
        bytes32 _paymentDate,
        bytes32[100] memory _msg,
        uint256 _orderAmt
    ) public {
        records[_id].setDeliveryDate(_dateDelivery);
        records[_id].setPaymentDate(_paymentDate);
        records[_id].setOrderDetails(_msg);
        records[_id].setOrderAmt(_orderAmt);

    }

    function getInitial(bytes32 _id)
        public
        view
        returns (bytes32, bytes32, bytes32[100] memory, uint256)
    {
        return (
            records[_id].getDeliveryDate(),
            records[_id].getPaymentDate(),
            records[_id].getOrderDetails(),
            records[_id].getOrderAmt()
        );

    }

    function setSellerFinal(
        bytes32 _id,
        bool _sellerApproval,
        uint256 _workingCapital,
        bytes32 _workingCapitalDeadline
    ) public {
        records[_id].setApprovalSeller(_sellerApproval);
        records[_id].setWorkingCapital(_workingCapital);
        records[_id].setWorkingCapitalDeadline(_workingCapitalDeadline);

    }

    function getSellerFinal(bytes32 _id)
        public
        view
        returns (bool, uint256, bytes32)
    {
        return (
            records[_id].getApprovalSeller(),
            records[_id].getWorkingCapital(),
            records[_id].getWorkingCapitalDeadline()
        );
    }

    function setBuyerFinal(
        bytes32 _id,
        uint256 _backingPercent,
        bool _buyerApproval,
        uint256 _interestRate
    ) public {
        records[_id].setBackingPercent(_backingPercent);
        records[_id].setApprovalBuyer(_buyerApproval);
        records[_id].setInterestRate(_interestRate);
    }

    function getBuyerFinal(bytes32 _id)
        public
        view
        returns (uint256, bool, uint256)
    {
        return (
            records[_id].getBackingPercent(),
            records[_id].getBuyerApproval(),
            records[_id].getInterestRate()
        );
    }

    function addInvestor(bytes32 _id, address _investor, uint256 _investment)
        public
    {
        records[_id].addInvestor(_investor, _investment);
    }

    function getInvestors(bytes32 _id) public view returns (address[] memory) {
        return records[_id].getInvestors();
    }

    function setOrderCompletion(bytes32 _id, bool _orderCompletion) public {
        records[_id].setOrderCompletion(_orderCompletion);
        records[_id].finalPayment();

    }

    function cashOut(address _from, uint256 tokens) public {
        token.cashOut(_from, tokens);
    }

    function transfer(address _to, uint256 tokens) public {
        token.transfer(_to, tokens);
    }

    function getBalance(address _user) public view returns (uint256) {
        return token.balanceOf(_user);
    }

}
