
let btn =  document.getElementById('heartIcon');

for(var i=0; i< btn.length; i++){
    btn[i].addEventListener('click', function(e){
       e.preventDefault();
        let Id  = this.dataset.PostId
        var action = this.dataset.action

        console.log('id:',Id  )
        console.log('user:',user)

        if(user === 'AnonymousUser')
        {
            alert('for like you have to login')

        }else
        {
            Post_like(Id , action )   
        }
    });
 
}
           function  Post_like(Id , action)
                { 
                console.log('user is log in sending data...')
        
                fetch('/like/',{
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body:JSON.stringify({'id':Id ,'action':action})
                })
                .then((response) =>{
                    if(!response.ok){
                        //error processing
                        throw 'Error'
                    }
                    return response.json()
                })
            
                .then((data) =>{
                    console.log('data:', data)
                    location.reload()
                })
            }

// $(document).ready(function(){

//     var csrf =$("input[name=csrfmiddlewaretoken]").val();
//     $('#heartIcon').on('click' , function(){

//         if (user === "AnonymousUser"){

//             console.log("user not connect")

//         }else{
//             $.ajax({
//                 url: '/like/',
//                 type: 'post',
//                 data:{
//                     post_id: $(this).attr('PostId'),
//                     csrfmiddlewaretoken: csrf,
        
//                 },
//                 success:function(response){
                    
//                 }
//             })
            
//         }
     
//     })
    


// })




    



     



