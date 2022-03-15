function deleteNote(noteId){
    fetch('/delete-note', //send POST request to /delete-note endpoint
    {method:"POST",
    body:JSON.stringify({ noteId: noteId })
    }).then((_res)=>{
        window.location.href='/';
        //refresh the homepage
    });
}