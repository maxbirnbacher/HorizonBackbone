document.addEventListener("DOMContentLoaded", function() {
    var startButton = document.getElementById("button_start_campaign_wizzard");
    var emptyStateDiv = document.getElementById("empty_campaign_state");
    var campaignStep1DialogDiv = document.getElementById("campaign_dialog_step1");
    var campaignStep2DialogDiv = document.getElementById("campaign_dialog_step2");
    var campaignStep3DialogDiv = document.getElementById("campaign_dialog_step3");
    var nextButtonStep1 = document.getElementById("wizzard-step1-button-next");
    var nextButtonStep2 = document.getElementById("wizzard-step2-button-next");
    var nextButtonStep3 = document.getElementById("wizzard-step3-button-next");
    var backButtonStep2 = document.getElementById("wizzard-step2-button-back");
    var backButtonStep3 = document.getElementById("wizzard-step3-button-back");
    var backButtonStep4 = document.getElementById("wizzard-step4-button-back");
    var cancelButtonStep1 = document.getElementById("wizzard-step1-button-cancel");
    var cancelButtonStep2 = document.getElementById("wizzard-step2-button-cancel");
    var cancelButtonStep3 = document.getElementById("wizzard-step3-button-cancel");
    var cancelButtonStep4 = document.getElementById("wizzard-step4-button-cancel");
    var encryptionKeyButton = document.getElementById("wizzard-form-button-encryption-key");

    let campaignDetails = []

    startButton.addEventListener("click", function() {
        emptyStateDiv.style.display = "none";
        campaignStep1DialogDiv.style.display = "block";
    });

    nextButtonStep1.addEventListener("click", function() {
        var campaignName = document.getElementById("wizard-form-field-name").value;
        var campaignDescription = document.getElementById("wizard-form-field-description").value;
        var campaignStartDate = document.getElementById("wizard-form-field-start-date").value;
        var campaignEndDate = document.getElementById("wizard-form-field-end-date").value;
        var campaignTarget = document.getElementById("wizard-form-field-target").value;

        // validate input
        if (campaignName == "") {
            alert("Please enter a name for your campaign.");
            return;
        }
        if (campaignDescription == "") {
            campaignDescription = "No description provided.";
        }
        if (campaignStartDate == "") {
            campaignStartDate = "0000-00-00"
        }
        if (campaignEndDate == "") {
            campaignEndDate = "0666-06-06"
        }
        if (campaignTarget == "") {
            campaignTarget = "No specific target provided.";
        }

        // create campaign object
        campaignDetails.push({
            "name": campaignName,
            "description": campaignDescription,
            "target": campaignTarget,
            "startDate": campaignStartDate,
            "endDate": campaignEndDate
        });

        campaignStep1DialogDiv.style.display = "none";
        campaignStep2DialogDiv.style.display = "block";
    });

    nextButtonStep2.addEventListener("click", function() {
        campaignStep2DialogDiv.style.display = "none";
        campaignStep3DialogDiv.style.display = "block";
    });

    nextButtonStep3.addEventListener("click", function() {
        campaignStep3DialogDiv.style.display = "none";
        emptyStateDiv.style.display = "block";
    });

    backButtonStep2.addEventListener("click", function() {
        campaignStep2DialogDiv.style.display = "none";
        campaignStep1DialogDiv.style.display = "block";

        // fill in form fields with previously entered data
        document.getElementById("wizard-form-field-name").value = campaignDetails[0].name;
        document.getElementById("wizard-form-field-description").value = campaignDetails[0].description;
        document.getElementById("wizard-form-field-target").value = campaignDetails[0].target;
        document.getElementById("wizard-form-field-start-date").value = campaignDetails[0].startDate;
        document.getElementById("wizard-form-field-end-date").value = campaignDetails[0].endDate;
    });

    backButtonStep3.addEventListener("click", function() {
        campaignStep3DialogDiv.style.display = "none";
        campaignStep2DialogDiv.style.display = "block";
    });

    backButtonStep4.addEventListener("click", function() {
        emptyStateDiv.style.display = "none";
        campaignStep3DialogDiv.style.display = "block";
    });

    cancelButtonStep1.addEventListener("click", function() {
        campaignStep1DialogDiv.style.display = "none";
        emptyStateDiv.style.display = "block";
    });

    cancelButtonStep2.addEventListener("click", function() {
        campaignStep2DialogDiv.style.display = "none";
        emptyStateDiv.style.display = "block";
    });

    cancelButtonStep3.addEventListener("click", function() {
        campaignStep3DialogDiv.style.display = "none";
        emptyStateDiv.style.display = "block";
    });

    cancelButtonStep4.addEventListener("click", function() {
        emptyStateDiv.style.display = "none";
        campaignStep3DialogDiv.style.display = "block";
    });

    encryptionKeyButton.addEventListener("click", function() {
        alert("Generating random encryption key...")
        // TODO: replace with a more secure method of generating a random encryption key that is server-side
        // create a random encryption key
        var randomEncryptionKey = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (var i = 0; i < 16; i++) {
            randomEncryptionKey += possible.charAt(Math.floor(Math.random() * possible.length));
        }

        // fill in form field with random encryption key
        document.getElementById("wizard-form-field-encryption-key").value = randomEncryptionKey;
    });

});