
// var todoitems = null;
var itemInput = document.querySelector("#item");

var todoid = null;
// hideContent();

var createToDoList = function (item) {
  var data = "item" + encodeURIComponent(item);
  fetch("https://fathomless-forest-99597.herokuapp.com/todoitems", {
    method: 'POST',
    body: data,
    credentials: 'include',
    headers: {
      "Content-type": "application/x-www-form-urlencoded"
    }
  // this code happens after you have been notified that mail is in the mailbox
  }).then(function (response) {
    console.log("item saved.");
    // load the new list of items
    getToDo();
  });
};

var getItem = function (id) {
  console.log('getitem', id)
  fetch(`https://fathomless-forest-99597.herokuapp.com/todoitems/${id}`, {
    method: 'GET',
    credentials: 'include',
    headers: {
      "Content-type": "application/x-www-form-urlencoded"
    }
  // this code happens after you have been notified that mail is in the mailbox
  })
  .then(function(response) {
    return response.json()
  })
  .then(function(data) {
      // editInput.value = data.item
      console.log("item saved.",data);
      // load the new list of items
      // getToDo();
  })
};


var theButton = document.querySelector("#the-button");
theButton.onclick = function () {
  var itemInput = document.querySelector("#item");
  var data = itemInput.value;

  createToDoList(data);
};

var createToDoList = function () {
  var data = "item=" + encodeURIComponent(itemInput.value);
  // data += "&date=" + encodeURIComponent(dateInput.value);
  // data += "&done=" + encodeURIComponent(doneInput.value);
  
  console.log('item')

  fetch("https://fathomless-forest-99597.herokuapp.com/todoitems", {
    method: 'POST',
    body: data,
    credentials: 'include',
    headers: {
      "Content-type": "application/x-www-form-urlencoded"
    }
  }).then(function (response) {
    console.log("item saved.");
    // load the new list of restaurants!
    getToDo();
  });
};

var updateTodoitem = function (id) {
  // console.log("this is id", id)
  let item = document.getElementById('editInput').value
  // console.log('tesitng', item)
  var data = "item=" + encodeURIComponent(item);

  fetch(`https://fathomless-forest-99597.herokuapp.com/todoitems/${id}`, {
      method: 'PUT',
      body: data,
      credentials: 'include',
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
  }).then(function (response) {
    console.log("item updated")
    getToDo();
  });
};

var updateButton = document.getElementById("update")
  updateButton.innerHTML = "Update";
  updateButton.onclick = function () {
    updateTodoitem(todoid)
    hideDiv()
  };


function showDiv() {
  var x = document.querySelector("#editItem");
  x.style.display = "block"
};

function hideDiv() {
  var x = document.getElementById("editItem");
  x.style.display = "none"
};

function hideContent() {
  var x = document.getElementById("#c");
  x.style.display = "none"
};
hideDiv();

var deleteTodoitem = function (id) {
  fetch(`https://fathomless-forest-99597.herokuapp.com/todoitems/${id}`, {
      method: 'DELETE',
      credentials: 'include',
  }).then(function (response) {
    console.log("item deleted")
    getToDo();
  });
};


var getLogin = function () {
  var loginButton = document.querySelector("#login-button");
  loginButton.onclick = function () {
    var emailInput = document.querySelector("#email");
    var data = emailInput.value;
    
    hideContent();
    // write retrieve email code here
  };
};

var checkUsernameExists = function () {
  var eInput = document.querySelector("#email")
  var passInput = document.querySelector("#password")
  console.log("email", eInput.value)
  console.log("password", passInput.value)
   var data = "email=" + encodeURIComponent(eInput.value);
   data += "&password=" + encodeURIComponent(passInput.value);  
   console.log('mydata: ', data)
   fetch("https://fathomless-forest-99597.herokuapp.com/sessions", {
     method: 'POST',
     body: data,
     credentials: 'include',
     headers: {
       "Content-type": "application/x-www-form-urlencoded"
     }
   }).then(function (response) {
     if (response.status == 401) {
        alert('error occured try again')
     }
    if (response.status == 201) {
      console.log("user exists.");
      getToDo();
    }
   });
 };

var loginButton = document.querySelector("#submit-login");
  var eInput = document.querySelector("#email")
  var passInput = document.querySelector("#password")
    // if (loginButton.disabled = true && eInput.value == "" & passInput == "") {
    //   alert("email and password must be filled out")
    //   loginButton.disabled = true;
    // }
    // else if (eInput.value != "" & passInput != ""){
    //   loginButton.disabled = false;
    // }
  loginButton.onclick = function () {
    console.log("login clicked")
    checkUsernameExists()
    // handleUserCreate()
    // showDiv();
    // hideLogin();
    // showContent();
    // getToDo();
  };

  var registerButton = document.querySelector("#register");
  registerButton.onclick = function () {
    console.log("register clicked")
    // showDiv();
    hideLogin();
    showRegister();
    // showContent();
    // getToDo();
  };


  var createUser = function () {
   var fnameInput = document.querySelector("#fname")
   var lnameInput = document.querySelector("#lname")
   var emailInput = document.querySelector("#emailr")
   var passwordInput = document.querySelector("#passwordr")
   console.log("fname", fnameInput.value)
   console.log("lname", lnameInput.value)
   console.log("fname", emailInput.value)
   console.log("lname", passwordInput.value)
    var data = "fname=" + encodeURIComponent(fnameInput.value);
    data += "&lname=" + encodeURIComponent(lnameInput.value);
    data += "&email=" + encodeURIComponent(emailInput.value);
    data += "&password=" + encodeURIComponent(passwordInput.value);  
    console.log('mydata: ', data)
    fetch("https://fathomless-forest-99597.herokuapp.com/users", {
      method: 'POST',
      body: data,
      credentials: 'include',
      headers: {
        "Content-type": "application/x-www-form-urlencoded"
      }
    }).then(function (response) {
      if (response.status == 401) {
        alert('error occured try again')
      }
     if (response.status == 422) {
      alert('error something went wrong with email or username')
    }
    if (response.status == 201) {
      console.log("user exists.");
      getToDo();
    }
      console.log("user saved.");
    });
  };

  var registerSubmitButton = document.querySelector("#submit-register");
  registerSubmitButton.onclick = function () {
    createUser();
    console.log("submit register clicked")
    // showDiv();
    showLogin();
    hideRegister();
    // showContent();
    // getToDo();
  };

function hideContent() {
  var x = document.getElementById("c");
  x.style.display = "none"
};

function showContent() {
  var x = document.getElementById("c");
  x.style.display = "block"
};

function hideRegister() {
  var x = document.getElementById("register-page");
  x.style.display = "none"
};

function showRegister() {
  var x = document.getElementById("register-page");
  x.style.display = "block"
};

// function showDiv() {
//   var x = document.querySelector("#editItem");
//   x.style.display = "block"
// };

// function showLogin() {
//   var x = document.getElementById("login-page");
//   x.style.display = "block"
// };
function showLogin() {
  var x = document.getElementById("login-page");
  x.style.display = "block"
};

function hideLogin() {
  var x = document.getElementById("login-page");
  x.style.display = "none"
};

  var getToDo = function () {
    fetch("https://fathomless-forest-99597.herokuapp.com/todoitems", {credentials: 'include'}).then(function (response) {

    if(response.status == 401) {
      console.log("401 was given.")
      showLogin();
      hideRegister();
      hideContent()
      // TODO; show login/register forms
    }
     else if (response.status != 200) {
      hideRegister();
      showLogin();
      hideContent();
      return;
    }

    else {
      response.json().then(function (data) {
        hideLogin()
        hideRegister()
        
        showContent()
        // show the appropriate div's for the datat



        // save all of the data into a global variable (to use later)
        todoitem = data;
        console.log("the data is", data);

        // data is an array of string values
        var suggestionsList = document.querySelector("#suggestions");
        suggestionsList.innerHTML = "";

        // add the items to the suggestions list
        data.forEach(function (todoitem) { // for restaurant in data
            var newItem = document.createElement("li");
            newItem.innerHTML = todoitem.item;
            suggestionsList.appendChild(newItem);

        var deleteButton = document.createElement("button");
        deleteButton.innerHTML = "Delete";
        deleteButton.onclick = function () {
          console.log(todoitem.id);
          var proceed = confirm(`Do you want to delete ${todoitem.item}?`);
          if (proceed) {
            deleteTodoitem(todoitem.id);
          }
        };
        newItem.appendChild(deleteButton);

        var editButton = document.createElement("button");
        editButton.innerHTML = "Edit";
        editButton.onclick = function () {
          console.log('edit', todoitem.id);
          var proceed = confirm(`Do you want to edit ${todoitem.item}?`);
          if (proceed) {
            console.log("testin todoitem id", todoitem.id)
            // updateTodoitem(todoitem.id)
            getItem(todoitem.id);
            todoid = todoitem.id;
            showDiv();
        }
      };
        newItem.appendChild(editButton);
      });
    });
};
});
};

getToDo();