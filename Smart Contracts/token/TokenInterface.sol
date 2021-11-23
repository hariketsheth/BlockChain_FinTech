pragma solidity >=0.4.21 <0.7.0;

abstract contract  TokenInterface {
    uint256 public totalSupply;

    function balanceOf(address _owner) virtual public view returns (uint256 balance);

    function transfer(address _to, uint256 _value)
        public virtual
        returns (bool success);

    function transferFrom(address _from, address _to, uint256 _value)
        public virtual
        returns (bool success);

    function approve(address _spender, uint256 _value)
        public virtual 
        returns (bool success);

    function allowance(address _owner, address _spender)
        public virtual
        view
        returns (uint256 remaining);

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(
        address indexed _owner,
        address indexed _spender,
        uint256 _value
    );
}
