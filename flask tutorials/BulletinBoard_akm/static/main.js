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
    //$('.download_btn').click(function() {
    //    location.href = "http://localhost:5000/download_file"
    //    console.log("http://localhost:5000/download_file")
    //});
});