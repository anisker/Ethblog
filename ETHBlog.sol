pragma solidity >=0.4.22 <0.7.0;

contract ETHBlog{
    
    event NewPost(uint postId, string title);
    
    mapping(string => uint[]) public usernamesPosts;
    mapping (uint => address) public postToOwner;
    mapping (string => uint) public ownerPostCount;
    
    struct Post{
        string username;
        string date;
        string title;
        string content;
    }
    
    Post[] public posts;
    
    modifier onlyOwner(uint _postId){
        require(msg.sender == postToOwner[_postId]);
        _;
    }
    
    function getNumberOfPosts() public view returns (uint){
        return posts.length;
    }
    
    function createPost(string memory _username, string memory _date, string memory _title,string memory _content) public{
        uint id = posts.length;
        posts.push(Post(_username,_date, _title, _content));
        usernamesPosts[_username].push(id);
        postToOwner[id] = msg.sender;
        ownerPostCount[_username]++;
        emit NewPost(id, _title);
    }
    
    function setPost (uint _postId, string calldata _title, string calldata _content) external onlyOwner(_postId){
        posts[_postId].title = _title;
        posts[_postId].content = _content;
    }
    
    function getPost(uint _postId) external view returns (string memory, string memory , string memory, string memory){
        return (posts[_postId].username,posts[_postId].date,posts[_postId].title,posts[_postId].content);
    }
}