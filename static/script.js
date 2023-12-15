$(function () {
    // Variables for the code
    let i = 0;
    let event;
    let city_name;
    // Checks if there is already content in the local storage `#history_0` if not will set it to `New York`
    if(localStorage.getItem("#history_0") == null){
        $("#city").text(city_name)
    }else{
        // If `#history_0` has content will display it
        $("#history_0").text(localStorage.getItem("#history_0"))
        // $("#city").text(localStorage.getItem("#history_0"))
        i++;
    }
    
    // Event listener for the search button to be clicked
    $("#search_btn").on("click", function(){
        // Sets event to the value of the entered in text in search field
        event = $(this).siblings("#city_input").val();
        console.log('event', event);
        if(event != null){
            city_name = event
            // get_weather()
            // Set text content for the document elements "#city" and "#history_{i}"
            // i being the variable i
            // $("#city").text(event)
            $(`#history_${i}`).text(`${event}`)
            // Sets the local storage
            localStorage.setItem(`#history_${i}`,event);
            $(`#history_${i}`).removeClass("invisible").addClass("visible");
            // Increaments the value of i by 1
            i++
            console.log("i",i);
            if(i>4){
                i = 0
            }
        }
    });


function show_local(){
    const num_elements = 5
    // For loop that iterates through each history storage keys
    // The changes the document display for the storage to visible if it is not null
    for(let q = 0; q < num_elements; q++){
        $(`#history_${q}`).text(localStorage.getItem(`#history_${q}`))
        if(localStorage.getItem(`#history_${q}`) != null){
            $(`#history_${q}`).removeClass("invisible").addClass("visible");
            }
        }
    };
// Event listener for buttons in the history and will call function to get weather of that city
$("#history").on("click", ".history_button", function(){
    let button_id = $(this).attr("id");
    let button_storage = localStorage.getItem(`#${button_id}`);
    $("#city").text(button_storage)
    city_name = button_storage
    // get_weather()
});

show_local();

});
