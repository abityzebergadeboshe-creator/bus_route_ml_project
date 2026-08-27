// ==============================
// GUZOAI JAVASCRIPT
// ==============================

// Confirm driver approval or rejection
document.addEventListener("DOMContentLoaded", function () {

    const approveButtons = document.querySelectorAll(".approve-btn");
    const rejectButtons = document.querySelectorAll(".reject-btn");

    approveButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to approve this driver?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    rejectButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to reject this driver?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });

});
