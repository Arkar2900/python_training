function alert_function() {
  var txt;
  if (confirm("Are you sure to delete!")) {
    document.location = '/delete';
    sessionStorage.setItem('to_delete_id', '');
    console.log('you click ok')
  }
  else {
    console.log('you click cancle')
  }
}