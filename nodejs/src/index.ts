import { readFile } from "fs/promises";
import { resolve } from "path";

// The text used to fill in the form (Japan Visitor Visa intake information)
const JAPAN_VISITOR_VISA_INTAKE_TEXT = "Full Name: STEVE RODGERS";

// API server URL and form ID to fill
const apiServer = "https://api.takeform.app";
const formId = "5c79b048-587b-4974-8f0d-afef0aa829e4";
let filledFormId = ""; // Variable to store the ID of the filled form

// Function to fill out the Japan Visa form
async function fillVisaJapan() {
  try {
    // Reading the content of the input file
    const filePath = resolve(__dirname, "../japan_visa_intake.txt");
    const buffer = await readFile(filePath); // Reading the file as a buffer
    const uint8Array = new Uint8Array(buffer); // Converting buffer to Uint8Array for transmission

    // Making a POST request to the API to fill the form
    const response = await fetch(
      `${apiServer}/developer/v1/forms/${formId}/fill`,
      {
        method: "POST",
        headers: {
          "X-API-Key": process.env.TAKEFORM_API_KEY || "", // API key for authentication
          "Content-Type": "application/json; charset=utf-8", // Content type of the request
        },
        body: JSON.stringify({
          sources: [
            {
              type: "Text", // First source: plain text
              text: JAPAN_VISITOR_VISA_INTAKE_TEXT, // The text used to fill the form
            },
            {
              type: "SourceFile", // Second source: file content
              content_type: "plain/text", // Content type of the file
              data: Array.from(uint8Array), // Converting Uint8Array to an array for transmission
            },
          ],
        }),
      },
    );

    // Parsing the response data
    const data = await response.json();
    console.log("Fill Japan Visa Response", data);

    // If the form was successfully filled, store the filled form ID
    if (data) {
      filledFormId = data["id"];
    }
  } catch (err) {
    console.error("❌ Error while filling the form:", err);
  }
}

// Helper function to pause execution for a set amount of time
const timer = (ms: number) => new Promise((res) => setTimeout(res, ms));

// Function to check the status of the filled form and download it once completed
async function getFilledFormDownloadUrl() {
  console.log("Checking filled form job", filledFormId);

  while (true) {
    await timer(10000); // Wait for 10 seconds before checking again
    try {
      // Making a GET request to check the status of the filled form
      const response = await fetch(
        `${apiServer}/developer/v1/filled-forms/${filledFormId}`,
        {
          method: "GET",
          headers: {
            "X-API-Key": process.env.TAKEFORM_API_KEY || "", // API key for authentication
          },
        },
      );

      const data = await response.json();

      // If the form is done, proceed to download it
      if (data["status"] === "Done") {
        // Making another GET request to retrieve the download URL for the filled form
        const downloadResponse = await fetch(
          `${apiServer}/developer/v1/filled-forms/${filledFormId}/download-url`,
          {
            method: "GET",
            headers: {
              "X-API-Key": process.env.TAKEFORM_API_KEY || "", // API key for authentication
            },
          },
        );

        const downloadData = await downloadResponse.json();
        console.log("DOWNLOAD FILLED FORM AT", downloadData); // Logging the download URL
        break; // Exit the loop once the form is downloaded
      }
    } catch (err) {
      console.error("❌ Error while checking the form status:", err);
    }
  }
}

// Main function to fill the form and download it once it's completed
const fillAndDownload = async () => {
  // Start by filling the Japan visa form
  await fillVisaJapan();

  // After the form is filled, check for completion and download the form
  await getFilledFormDownloadUrl();
};

// Execute the function to fill the form and download it
fillAndDownload();
