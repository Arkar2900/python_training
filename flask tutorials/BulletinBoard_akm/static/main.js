//function alert_function() {
//  var txt;
//  if (confirm("Are you sure to delete!")) {
//    document.location = '/delete';
//    sessionStorage.setItem('to_delete_id', '');
//    console.log('you click ok')
//  }
//  else {
//    console.log('you click cancle')
//  }
//}
//
//// Example POST method implementation:
//async function postData(url = '', data = {}) {
//  // Default options are marked with *
//  const response = await fetch(url, {
//    method: 'POST', // *GET, POST, PUT, DELETE, etc.
//    mode: 'cors', // no-cors, *cors, same-origin
//    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
//    credentials: 'same-origin', // include, *same-origin, omit
//    headers: {
//      'Content-Type': 'application/json'
//      // 'Content-Type': 'application/x-www-form-urlencoded',
//    },
//    redirect: 'follow', // manual, *follow, error
//    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
//    body: JSON.stringify(data) // body data type must match "Content-Type" header
//  });
//  return response.json(); // parses JSON response into native JavaScript objects
//}



//function alert_function() {
//  //var element = document.getElementsByClassName("to_delete");
//  var element = document.querySelector(".to_delete")
//  to_delete_id = element.id
//  console.log(document.querySelector(".to_delete"))
//  if (confirm("Are you sure to delete!")) {
//
//    console.log('you click ok')
//    _id = parseInt(to_delete_id)
//    //console.log('you delete at ' + str)
//    console.log(_id)
//    console.log("http://localhost:5000/delete/"+_id)
//    //window.location.href = "http://localhost:5000/delete/"+_id
//    //fetch(str)
//    //.then(data => {
//    //  console.log(data); // JSON data parsed by `data.json()` call
//    //});
//      }
//  else {
//    console.log('you click cancle')
//    window.location.href = "http://localhost:5000/users"
//  }
//}

$(document).ready(function () {
    $('.to_delete').click(function() {
      var id = $(this).attr('id');
      //alert(id);
      if (confirm("Are you sure to delete?")) {
        console.log('this is id'+ id)
        location.href = "http://localhost:5000/delete/" + id
        console.log("http://localhost:5000/delete/" + id)

      }
      else {
        console.log('You click cancle!')
        location.href = 'http://localhost:5000/users'
        console.log('http://localhost:5000/users')
      }
    });
    $('.to_delete_post').click(function() {
      var id = $(this).attr('id');
      //alert(id);
      if (confirm("Are you sure to delete?")) {
        console.log('this is id'+ id)
        location.href = "http://localhost:5000/delete_post/" + id
        console.log("http://localhost:5000/delete_post/" + id)

      }
      else {
        console.log('You click cancle!')
        location.href = 'http://localhost:5000/posts'
        console.log('http://localhost:5000/posts')
      }
    });
});