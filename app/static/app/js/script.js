var likeButton = document.getElementById("like-btn-{{ post.id }}");
var csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

likeButton.addEventListener("click", function(event) {
    event.preventDefault();
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{% url 'post_like' post.id %}");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    xhr.onload = function() {
        if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        likeButton.innerHTML = "<i class='fa-regular fa-heart'></i>" + response.likes_count;
        } else {
        console.log("Houve um erro ao adicionar o like.");
        }
    };
    xhr.send();
});