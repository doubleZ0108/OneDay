const localStorageName = 'user-name';

const signUpButton = document.getElementById('signUp');
const accountSignUpButton = document.getElementById('accountSignUp');
const signInButton = document.getElementById('signIn');
const accountSignInButton = document.getElementById('accountSignIn');

const signUpName = document.getElementById('signUpName');
const signUpPassword = document.getElementById('signUpPassword');
const signInName = document.getElementById('signInName');
const signInPassword = document.getElementById('signInPassword');

const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

accountSignUpButton.addEventListener('click', () => {
    let name = signUpName.value;
    let password = signUpPassword.value;
    console.log(name+" " + password);
    //Todo: 将[name, password]传给后端，记录用户名称和密码
    let userpassword = "{username:"+name+",password:"+password+"}";
    receiveSignUp(userpassword);
    const hiddenText = document.getElementById('success-sign-up');
    hiddenText.className = 'show';
    setTimeout("window.location.reload()",1000);
});

accountSignInButton.addEventListener('click', () => {
    let name = signInName.value;
    let password = signInPassword.value;
    console.log(name+" " + password);  //Test
    //Todo: 将[name, password]传给后端，判断正确还是错误，返回pass
    let pass = true;  //Test
    if(pass) {
        const hiddenTextForSuccess = document.getElementById('success-sign-in');
        hiddenTextForSuccess.className = 'show';
        localStorage.setItem(localStorageName, name);
        // window.location.href="incex.html";
        window.location.href="calendar.html";
//        setTimeout("window.location.href=\"calendar.html\" ",300);
    }
    else{
        const hiddenTextForFail = document.getElementById('fail-sign-in');
        hiddenTextForFail.className = 'show';
    }
});