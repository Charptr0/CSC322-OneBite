//Comment
function showComment(){
    var commentArea = document.getElementById("comment-area");
    //commentArea.classList.remove("hide");
    commentArea.setAttribute("style","display:block");
}

//Reply
function showReply(){
    var replyArea = document.getElementById("reply-area");
    replyArea.classList.remove("hide");
}