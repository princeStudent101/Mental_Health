const form = document.querySelector("#checkin-form");
const submitButton = document.querySelector("#submit-button");
const errorMessage = document.querySelector("#error-message");
const result = document.querySelector("#result");
const resultScore = document.querySelector("#result-score");
const editAnswersButton = document.querySelector("#edit-answers");

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function hideError() {
  errorMessage.textContent = "";
  errorMessage.hidden = true;
}

function getPayload(formData) {
  return {
    age: Number(formData.get("age")),
    gender: formData.get("gender"),
    Country: formData.get("Country"),
    academic_level: formData.get("academic_level"),
    most_used_platform: formData.get("most_used_platform"),
    purpose_of_use: formData.get("purpose_of_use"),
    avg_daily_usage_hours: Number(formData.get("avg_daily_usage_hours")),
    daily_unlocks: Number(formData.get("daily_unlocks")),
    study_hours: Number(formData.get("study_hours")),
    physical_activity_hours: Number(formData.get("physical_activity_hours")),
    sleep_hours_per_night: Number(formData.get("sleep_hours_per_night")),
    stress_level: formData.get("stress_level"),
  };
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();

  if (!form.reportValidity()) {
    return;
  }

  submitButton.disabled = true;
  submitButton.querySelector(".button-label").textContent = "Preparing your check-in…";

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(getPayload(new FormData(form))),
    });
    const data = await response.json();

    if (!response.ok) {
      const details = Array.isArray(data.detail)
        ? data.detail.map((issue) => issue.msg).join(" ")
        : data.detail;
      throw new Error(details || "We couldn't process your answers. Please check the fields and try again.");
    }

    resultScore.textContent = data.predict_mental_health_score;
    form.hidden = true;
    result.hidden = false;
    result.scrollIntoView({ behavior: "smooth", block: "center" });
  } catch (error) {
    showError(error instanceof Error ? error.message : "Something went wrong. Please try again.");
  } finally {
    submitButton.disabled = false;
    submitButton.querySelector(".button-label").textContent = "Get my check-in";
  }
});

editAnswersButton.addEventListener("click", () => {
  result.hidden = true;
  form.hidden = false;
  hideError();
  form.scrollIntoView({ behavior: "smooth", block: "start" });
});
