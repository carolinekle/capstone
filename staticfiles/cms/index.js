tinymce.init({
    selector: '#content-field',
    plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount linkchecker',
    toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
    height: '500',
    width:'800',
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name',
    mergetags_list: [
      { value: 'First.Name', title: 'First Name' },
      { value: 'Email', title: 'Email' },
    ],
    
});

document.addEventListener('DOMContentLoaded', () => {

/*   let btnContainer = document.querySelector('.dash');

  let error =document.querySelector('.errorlist')
  const input = document.querySelector('#imageInput');   */
  input = document.getElementById('id_main')
  input.addEventListener('change', function() {
  
    const image_id = this.value;
    console.log("id: "+image_id)
    if (image_id) {
      fetch(`/get_image_url/${image_id}/`)
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          const imageUrl = data.image_url;
          if (imageUrl) {
              let img = document.createElement('img');
              img.setAttribute('id', 'imagePreview');
              img.style.display = "block";
              img.classList.remove('m-2');
              img.src = imageUrl;
              input.insertAdjacentElement("beforebegin", img);
          }
      })
      .catch(error => console.error('Error fetching image URL:', error));
    }
  })  

})
/* 

  let select =document.querySelector('#imageSelect')
  console.log("select"+ select)
  select.addEventListener('change', function(event) {
 
    const selectedOption = event.target.selectedOptions[0];
    console.log(selectedOption)
    imageUrl = selectedOption.value
  
    if (imageUrl) {
      imagePreview.src = imageUrl;
      imagePreview.style.display = 'block';
    } else {
      imagePreview.style.display = 'none';
    }
  });


if(input){
  input.addEventListener('change', function(event) {
      const imagePreview = document.getElementById('imagePreview');
      const file = event.target.files[0]
      
      if (file) {
          const imageURL = URL.createObjectURL(file);
          imagePreview.src = imageURL
          imagePreview.style.display = 'block'
      } else {
          imagePreview.style.display = 'none'
      }
  });
}

  if (error){
    error.classList.add("alert alert-warning")
  }
  

});

 */