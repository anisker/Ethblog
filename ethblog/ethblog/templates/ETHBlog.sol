pragma solidity >=0.4.22 <0.7.0;


contract ETHBlog{
    
    event NewUser(uint UserId, string email);
    
    mapping (uint => address) public userToOwner;
    mapping (address => uint) ownerUserCount;
    
    struct User{
        uint hashed_password;
        string username;
        string email;
        string posts;
    }
    
    
    User[] public users;
    
    modifier onlyOwner(uint _userId){
        require(msg.sender == userToOwner[_userId]);
        _;
    }
    
    function _generateUser(uint _hashed_password ,string memory _username, string memory _email, string memory _posts) private{
        users.push(User(_hashed_password,_username,_email,_posts));
        uint id = users.length -1;
        userToOwner[id] = msg.sender;
        ownerUserCount[msg.sender]++;
        emit NewUser(id, _email);
    }
    
    function createUser(string memory _username, string memory _email, uint _hashed_password, string memory _posts) public{
        require(ownerUserCount[msg.sender] == 0);
        _generateUser(_hashed_password, _username,_email,_posts);
    }
    
    function setUsername(string calldata _email, uint _userId) external onlyOwner(_userId){
        users[_userId].email=_email;
    }
    
    function setHashed_password (uint _hashed_password, uint _userId) external onlyOwner(_userId){
        users[_userId].hashed_password=_hashed_password;
    }
    
    function setPosts (string calldata _date, string calldata _title, string calldata _content, uint _userId) external onlyOwner(_userId){
        users[_userId].posts=string((abi.encodePacked(users[_userId].posts,"-",_date,"-",_title,"-",_content,"-")));
    }
    
    function getUsername(uint _userId) external view returns (string memory){
        return users[_userId].username;
    }
    
    function getEmail(uint _userId) external view returns (string memory){
        return users[_userId].email;
    }
    
    function getPosts(uint _userId) external view returns (string memory){
        return users[_userId].posts;
    }
}