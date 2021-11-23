import Web3 from "web3";
import TruffleContract from "truffle-contract";

const web3Provider = new Web3("https://testnetv3.matic.network");
// if (window.ethereum == "https: //testnetv3.matic.network") {}

ethereum.enable().then(account => {
    const defaultAccount = account[0];
    web3Provider.eth.defaultAccount = defaultAccount;
});

const contract = TruffleContract(
    [{
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_investor",
                    type: "address"
                },
                {
                    name: "_investment",
                    type: "uint256"
                }
            ],
            name: "addInvestor",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_from",
                    type: "address"
                },
                {
                    name: "tokens",
                    type: "uint256"
                }
            ],
            name: "cashOut",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                name: "_id",
                type: "bytes32"
            }],
            name: "createContract",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                name: "_address",
                type: "address"
            }],
            name: "register",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_buyer",
                    type: "address"
                }
            ],
            name: "setBuyer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_backingPercent",
                    type: "uint256"
                },
                {
                    name: "_buyerApproval",
                    type: "bool"
                },
                {
                    name: "_interestRate",
                    type: "uint256"
                }
            ],
            name: "setBuyerFinal",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_dateDelivery",
                    type: "bytes32"
                },
                {
                    name: "_paymentDate",
                    type: "bytes32"
                },
                {
                    name: "_orderAmt",
                    type: "uint256"
                }
            ],
            name: "setInitial",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_orderCompletion",
                    type: "bool"
                }
            ],
            name: "setOrderCompletion",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_seller",
                    type: "address"
                }
            ],
            name: "setSeller",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_id",
                    type: "bytes32"
                },
                {
                    name: "_sellerApproval",
                    type: "bool"
                },
                {
                    name: "_workingCapital",
                    type: "uint256"
                },
                {
                    name: "_workingCapitalDeadline",
                    type: "bytes32"
                }
            ],
            name: "setSellerFinal",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            constant: false,
            inputs: [{
                    name: "_to",
                    type: "address"
                },
                {
                    name: "tokens",
                    type: "uint256"
                }
            ],
            name: "transfer",
            outputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "function"
        },
        {
            inputs: [],
            payable: false,
            stateMutability: "nonpayable",
            type: "constructor"
        },
        {
            constant: true,
            inputs: [{
                name: "_user",
                type: "address"
            }],
            name: "getBalance",
            outputs: [{
                name: "",
                type: "uint256"
            }],
            payable: false,
            stateMutability: "view",
            type: "function"
        },
        {
            constant: true,
            inputs: [{
                name: "_id",
                type: "bytes32"
            }],
            name: "getBuyerFinal",
            outputs: [{
                    name: "",
                    type: "uint256"
                },
                {
                    name: "",
                    type: "bool"
                },
                {
                    name: "",
                    type: "uint256"
                }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
        },
        {
            constant: true,
            inputs: [{
                name: "_id",
                type: "bytes32"
            }],
            name: "getInitial",
            outputs: [{
                    name: "",
                    type: "bytes32"
                },
                {
                    name: "",
                    type: "bytes32"
                },
                {
                    name: "",
                    type: "uint256"
                }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
        },
        {
            constant: true,
            inputs: [{
                name: "_id",
                type: "bytes32"
            }],
            name: "getInvestors",
            outputs: [{
                name: "",
                type: "address[]"
            }],
            payable: false,
            stateMutability: "view",
            type: "function"
        },
        {
            constant: true,
            inputs: [{
                name: "_id",
                type: "bytes32"
            }],
            name: "getSellerFinal",
            outputs: [{
                    name: "",
                    type: "bool"
                },
                {
                    name: "",
                    type: "uint256"
                },
                {
                    name: "",
                    type: "bytes32"
                }
            ],
            payable: false,
            stateMutability: "view",
            type: "function"
        }
    ],
    "0x08970FEd061E7747CD9a38d680A601510CB659FB"
);

contract.setProvider(web3.currentProvider);
contract.defaults({ from: web3Provider.eth.defaultAccount });



///web3.utils.fromAscii() -- for conversion to bytes32
