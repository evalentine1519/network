document.addEventListener('DOMContentLoaded', function() {

    let newChirpForm = document.querySelector('#new_chirp_box');
    if (newChirpForm != null) {
        newChirpForm.style.padding = '5px';
        newChirpForm.style.margin = '10px';
    }


    let chirpBoxList = document.querySelectorAll('.chirpbox');
    let editBoxList = document.querySelectorAll('.editbox');
    for (let i = 0; i < chirpBoxList.length; i++) {
        chirpBoxList[i].style.border = 'thin solid black';
        chirpBoxList[i].style.padding = '5px';
        chirpBoxList[i].style.margin = '10px';
        chirpBoxList[i].style.display = 'block'
        editBoxList[i].style.border = 'thin solid black';
        editBoxList[i].style.padding = '5px';
        editBoxList[i].style.margin = '10px';
        editBoxList[i].style.display = 'none'
    };

    let likeButtonList = document.querySelectorAll('.likebutton')
    for (let i = 0; i < likeButtonList.length; i++) {
        likeButtonList[i].addEventListener('click', likeHandler.bind(this));
    };

    let editButtonList = document.querySelectorAll('.editbutton');
    let saveButtonList = document.querySelectorAll('.savebutton');
    console.log(saveButtonList);
    for (let i=0; i<editButtonList.length; i++) {
        console.log(editButtonList.length);
        editButtonList[i].addEventListener('click', editHandler.bind(this));
        saveButtonList[i].addEventListener('click', editHandler.bind(this));
    };

    let followButton = document.querySelector('.followbutton');
    console.log(followButton);
    followButton.addEventListener('click', followHandler.bind(this));

    return false;
});

function followHandler(element) {
    console.log('follow button clicked');
    let profileUser = document.querySelector('#profileuser').innerText;
    console.log(profileUser);
    value = element.target.innerText;
    let option = '';
    let followCount = document.querySelector('#followercount');
    let count = parseInt(followCount.innerText);

    if (value == 'Follow') {
        element.target.innerText = 'Unfollow';
        option = 'setFollow';
        count++;
    } else if (value == 'Unfollow') {
        element.target.innerText = 'Follow';
        option = 'setUnfollow';
        count--;
    };

    followCount.innerText = count;

    fetch(`/chirp/${profileUser}`, {
        method: 'PUT',
        body: JSON.stringify({
            action: option
        })
    });
}

function editHandler(element) {
    value = element.target.innerText;
    chirpId = element.target.id;
    console.log(chirpId);
    console.log(`/chirp/${chirpId}`);
    editBox = element.target.parentElement.parentElement.querySelector('.editbox');
    console.log(editBox);
    chirpBox = element.target.parentElement.parentElement.querySelector('.chirpbox');
    edited = false;

    if (value === 'Edit Chirp') {
        editBox.style.display = 'block';
        chirpBox.style.display = 'none';
    } else if (value === 'Save Chirp') {
        editContent = editBox.querySelector('.textedit').value;
        chirpBox.querySelector('#chirp').innerText = editContent;
        editBox.style.display = 'none';
        chirpBox.style.display = 'block';
        edited = true;
        console.log('chirp id is: ' + chirpId);
        fetch(`/chirp/${chirpId}`, {
            method: 'PUT',
            body: JSON.stringify({
                action: 'Edit',
                context: editContent
            })
        });
    };


    return false;
}

function likeHandler(element) {
    console.log(element.target.parentElement);
    console.log(element.target.id);
    value = element.target.innerText;
    likecount = element.target.parentElement.querySelector('#likecount');
    chirpId = parseInt(element.target.id);
    console.log(chirpId);

    if (value === 'Like') {
        console.log("Like button clicked, switched to 'Unlike' button");
        likecount.innerText = parseInt(likecount.innerText) + 1;
        element.target.innerText = 'Unlike';
    } else {
        console.log("Unlike button clicked, switched to 'Like' button");
        likecount.innerText = parseInt(likecount.innerText) - 1;
        element.target.innerText = 'Like';
    }

    fetch(`/chirp/${chirpId}`, {
        method: 'PUT',
        body: JSON.stringify({
            action: `${value}`
        })
    });
}