pragma solidity >=0.4.21 <0.7.0;

import "./Registerations.sol";
import "../token/Token.sol";

contract SFCContracts {
    Token private token;

    bytes32 id;
    address buyer;
    address seller;
    mapping(address => uint256) investments;
    Registerations private registerations;

    address[] investors;

    bytes32 deliveryDate;
    bytes32 paymentDate;
    bytes32 workingCapitalDeadline;
    uint256 orderAmount;
    bytes32[100] orderDetails;

    uint256 workingCapital;
    bool approvalSeller;

    uint256 interestRate;
    uint256 backingPercent;

    bool approvalBuyer;
    bool orderCompletion;

    constructor(bytes32 _id) public {
        id = _id;

    }

    modifier checkUser(address _address) {
        require(registerations.isRegistered(_address), "Access Denied");
        _;
    }
    modifier onlyOnNum(uint256 num) {
        require(num != 0, "Value not set");
        _;
    }

    modifier onlyOnInvestors {
        require(investors.length != 0, "There are no investrors");
        _;
    }
    modifier onSellerTrue() {
        require(approvalSeller == true, "Seller hasn't agreed");

        _;
    }
    modifier onBuyerTrue() {
        require(approvalSeller == true, "Seller hasn't agreed");

        _;
    }
    modifier onlyOnSetAddress(address check) {
        require(check != address(0), "Value not yet set");
        _;
    }

    modifier onlyOnString(bytes32 str) {
        require(str.length != 0, "There are no investrors");
        _;
    }

    modifier checkWorkingCapitalDeadline() {
        require(
            workingCapitalDeadline.length != 0,
            "Working Capital Deadline not set"
        );
        _;
    }

    modifier onNumNull(uint256 num) {
        require(num == 0, "Value has already been set");
        _;
    }

    modifier onStringNull(bytes32 str) {
        require(str.length == 0, "Value has already been set");
        _;
    }
    modifier onUserNull(address user) {
        require(user == address(0), "Value already set");
        _;
    }

    modifier onBoolNull(bool val) {
        require(val == false, "Value already set");
        _;
    }

    modifier checkOrderCompletion(bool _orderCompletion) {
        require(_orderCompletion == true, "Order has to be completed");
        _;
    }

    ////////////////////////////////////////////
    function setInterestRate(uint256 _interestRate)
        public
        onNumNull(interestRate)
        onSellerTrue
    {
        interestRate = _interestRate;
    }

    function setDeliveryDate(bytes32 _deliveryDate)
        public
        onStringNull(deliveryDate)
    {
        deliveryDate = _deliveryDate;
    }
    function setBackingPercent(uint256 _backingPercent)
        public
        onNumNull(backingPercent)
        onSellerTrue
    {
        backingPercent = _backingPercent;
    }

    function setOrderAmt(uint256 _orderAmt) public onNumNull(orderAmount) {
        orderAmount = _orderAmt;
    }

    /////////////to update

    function setOrderDetails(bytes32[100] memory _msg) public {
        orderDetails = _msg;
    }

    function setWorkingCapital(uint256 _workingCapital)
        public
        onlyOnString(deliveryDate)
        onlyOnString(paymentDate)
        onlyOnOrderDetails
        onlyOnNum(orderAmount)
        onNumNull(workingCapital)
    {
        workingCapital = _workingCapital;
    }

    function setPaymentDate(bytes32 _paymentDate)
        public
        onStringNull(paymentDate)
    {
        paymentDate = _paymentDate;
    }

    function setOrderCompletion(bool _orderCompletion)
        public
        onSellerTrue
        onBuyerTrue
        onlyOnOrderDetails
        checkWorkingCapitalDeadline
        onlyOnNum(backingPercent)
        onlyOnNum(interestRate)
        onBoolNull(orderCompletion)
    {
        orderCompletion = _orderCompletion;
    }

    ///////////////////////////////////////////////////
    function setWorkingCapitalDeadline(bytes32 _deadline)
        public
        onlyOnString(deliveryDate)
        onlyOnString(paymentDate)
        onlyOnOrderDetails
        onlyOnNum(orderAmount)
        onStringNull(workingCapitalDeadline)
    {
        workingCapitalDeadline = _deadline;
    }
    function getWorkingCapitalDeadline()
        public
        view
        checkWorkingCapitalDeadline
        returns (bytes32)
    {
        return workingCapitalDeadline;
    }
    function setBuyer(address _buyer)
        public
        onUserNull(buyer)
        checkUser(_buyer)
    {
        buyer = _buyer;
    }

    function getBuyer() public view onlyOnSetAddress(buyer) returns (address) {
        return buyer;
    }
    function getSeller()
        public
        view
        onlyOnSetAddress(seller)
        returns (address)
    {
        return seller;
    }

    function getInvestors()
        public
        view
        onlyOnInvestors
        onBuyerTrue
        onSellerTrue
        returns (address[] memory)
    {
        return investors;
    }

    function getDeliveryDate()
        public
        view
        onlyOnString(deliveryDate)
        returns (bytes32)
    {
        return deliveryDate;
    }

    function getPaymentDate()
        public
        view
        onlyOnString(paymentDate)
        returns (bytes32)
    {
        return paymentDate;
    }

    function getOrderAmt() public view returns (uint256) {
        return orderAmount;
    }
    modifier onlyOnOrderDetails() {
        require(orderDetails.length != 0, "Order Details not set");
        _;
    }
    function getOrderDetails()
        public
        view
        onlyOnOrderDetails
        returns (bytes32[100] memory)
    {
        return orderDetails;
    }
    function getWorkingCapital() public view returns (uint256) {
        return workingCapital;
    }
    function getApprovalSeller() public view returns (bool) {
        return approvalSeller;
    }
    function getInterestRate() public view returns (uint256) {
        return interestRate;
    }
    function getBackingPercent() public view returns (uint256) {
        return backingPercent;
    }

    function getBuyerApproval() public view returns (bool) {
        return approvalBuyer;
    }

    function setSeller(address _seller)
        public
        onUserNull(seller)
        checkUser(_seller)
    {
        seller = _seller;
    }
    modifier investmentRequirement(uint256 _investment) {
        require(_investment < workingCapital, "Funds exceeded requirement ");
        _;
    }

    function addInvestor(address _investor, uint256 _investment)
        public
        investmentRequirement(_investment)
        onBuyerTrue
        onSellerTrue
        checkUser(_investor)
    {
        investors.push(_investor);
        investments[_investor] = _investment;

        workingCapital -= _investment;
        paymentToSeller(_investor, _investment);

    }

    function getInvestment(address _investor) public view returns (uint256) {
        return investments[_investor];
    }

    function setApprovalSeller(bool _approvalSeller)
        public
        onlyOnString(deliveryDate)
        onlyOnString(paymentDate)
        onlyOnOrderDetails
        onBoolNull(approvalSeller)
        onlyOnNum(orderAmount)
    {
        approvalSeller = _approvalSeller;
    }

    function setApprovalBuyer(bool _approvalBuyer)
        public
        onSellerTrue
        checkWorkingCapitalDeadline
        onBoolNull(approvalBuyer)
    {
        approvalBuyer = _approvalBuyer;
    }

    ////////////////////////////////////// ESCROW

    // function transferFrom(address _from, address _to, uint256 tokens) public{
    //     token.transferFrom(_from, _to, tokens);
    // }

    function paymentToSeller(address _investor, uint256 _investment)
        public
        onSellerTrue
        onBuyerTrue
        onlyOnOrderDetails
        checkWorkingCapitalDeadline
        onlyOnNum(backingPercent)
        onlyOnNum(interestRate)
    {
        token.transferFrom(_investor, seller, _investment);
    }

    function finalPayment() public checkOrderCompletion(orderCompletion) {
        for (uint256 i = 0; i < investors.length; i++) {
            orderAmount -= investments[investors[i]];
            token.transferFrom(buyer, investors[i], investments[investors[i]]);
        }

        token.transferFrom(buyer, seller, orderAmount);

    }

    // trasnferfrom

}
