<template>
  <v-app id="inspire">
    <v-app-bar class="px-3" density="compact" flat>
      <v-avatar
        class="hidden-md-and-up"
        color="grey-darken-1"
        size="32"
      ></v-avatar>

      <v-spacer></v-spacer>

      <v-tabs color="grey-darken-2" centered>
        <v-tab v-for="link in links" :key="link" :text="link"></v-tab>
      </v-tabs>
      <v-spacer></v-spacer>

      <v-avatar
        class="hidden-sm-and-down"
        color="grey-darken-1"
        size="32"
      ></v-avatar>
    </v-app-bar>

    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-row justify="center">
          <!-- First Div -->
          <v-col
            :cols="12"
            :md="showLoader ? 8 : showContent2 || showContent3 ? 5 : 8"
          >
            <v-sheet
              class="content-sheet content-redesign"
              min-height="70vh"
              rounded="lg"
            >
              <!-- Loader Section -->
              <div v-if="showLoader" class="d-flex justify-center">
                <v-progress-circular
                  indeterminate
                  color="primary"
                  size="64"
                ></v-progress-circular>
              </div>

              <div v-else>
                <h2
                  v-if="!imagePreview"
                  style="color: teal; font-family: 'Noto Sans Bengali', sans-serif; font-size: 30px;"
                  class="text-center mb-4"
                >
                  Select an Image to Identify Disease
                </h2>

                <!-- File Input -->
                <v-file-input
                  v-if="!imagePreview"
                  v-model="selectedImage"
                  accept="image/*"
                  label="Choose your image"
                  prepend-icon="mdi-camera"
                  outlined
                  class="file-input-custom"
                  dense
                ></v-file-input>

                <!-- Show Image Preview after prediction -->
                <v-img
                  v-if="imagePreview"
                  :src="imagePreview"
                  width="300"
                  height="300"
                  class="mx-auto image-preview"
                  :alt="'Uploaded Image Preview'"
                ></v-img>

                <v-btn
                  v-if="!showContent2 && selectedImage && !showLoader"
                  @click="() => { startPrediction();}"
                  color="teal"
                  class="mt-4 predict-btn"
                >
                  Predict
                </v-btn>
              </div>
            </v-sheet>
          </v-col>

          <!-- Second Div with Smooth Transition -->
            <v-col v-if="showContent2" :cols="12" :md="7">
              <v-sheet class="content-sheet" min-height="70vh" rounded="lg">
                <!-- Display response data -->
                <div v-if="responseData">
                  <span
                    style="
                      font-weight: bold;
                      font-size: 22px;
                      padding-right: 120px;
                      text-align: end;
                      font-family: 'Noto Sans Bengali', sans-serif;
                    "
                  >
                    Disease
                  </span>
                  <span
                    style="
                      font-weight: bold;
                      padding-right: 50px;
                      font-size: 22px;
                      text-align: end;
                      font-family: 'Noto Sans Bengali', sans-serif;
                    "
                  >
                    Confidence
                  </span>
                  <div
                    v-for="(prediction, index) in responseData.top_predictions"
                    :key="index"
                    class="prediction-item"
                  >
                    <div class="label-container">
                      <span
                        style="
                          font-weight: bold;
                          padding-right: 20px;
                          text-align: end;
                          font-family: 'Noto Sans Bengali', sans-serif;
                        "
                        class="class-name"
                      >
                        {{ classMapping[prediction.class] }}
                      </span>

                      <div class="bar-container">
                        <div class="bar-wrapper">
                          <v-progress-linear
                            color="teal"
                            height="30"
                            :model-value="valueConfidendce[index] * 100"
                          >
                            <strong
                              >{{
                                (prediction.confidence_score * 100).toFixed(2)
                              }}%</strong
                            >
                          </v-progress-linear>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else>
                  <p>No data available</p>
                </div>
              </v-sheet>
            </v-col>

          <!-- Third Div with Smooth Transition -->
          <v-col v-if="showContent3" :cols="12" :md="12" class="mt-5">
            <v-sheet class="content-sheet" min-height="70vh" rounded="lg">
              <div v-if="responseData">
                <div style="max-width: 800px; padding-bottom: 40px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h3 style="font-size: 23px; font-family: 'Noto Sans Bengali', sans-serif; margin: 0;">
                  {{ diseaseName }} - বিস্তারিত বিবরণ
                </h3>
                
                <div style="margin-top: 10px;">
                  <!-- Severity Level Title -->
                  <h4 style="font-size: 20px; font-family: 'Noto Sans Bengali', sans-serif; margin-bottom: 10px;">Severity Level</h4>
                  
                  <div style="background-color: #f9f9f9; border: 1px solid #e0e0e0; border-radius: 8px; padding: 5px;">
                    <!-- Progress Bar Container -->
                    <div style="display: flex; height: 20px; border-radius: 4px; overflow: hidden;">
                      <!-- Low Severity -->
                      <div style="width: 33.33%; background-color: #a3d0a0; height: 100%; opacity: 0.05;">
                      </div>
                      <!-- Moderate Severity -->
                      <div style="width: 33.33%; background-color: #f0a14e; height: 100%; opacity: 1;">
                      </div>
                      <!-- High Severity -->
                      <div style="width: 33.33%; background-color: #c72c3a; height: 100%; opacity: 0.05;">
                      </div>
                    </div>
                    <!-- Severity Description -->
                    <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                      <span style="color: #a3d0a0; font-weight: bold; font-family: 'Noto Sans Bengali', sans-serif;">Low</span>
                      <span style="color: #f0a14e; font-weight: bold; font-family: 'Noto Sans Bengali', sans-serif;">Moderate</span>
                      <span style="color: #c72c3a; font-weight: bold; font-family: 'Noto Sans Bengali', sans-serif;">High</span>
                    </div>
                  </div>
                </div>
              </div>



                <div 
                  style="text-align: justify; font-family: 'Noto Sans Bengali', sans-serif; max-width: 800px; font-weight: 500; font-size: 18px; overflow-x: hidden; margin: 0 auto;"
                  v-html="data_fetched.description">
                </div>
                <div style="margin-top: 10px; max-width: 800px; margin: 0 auto;">
                  <v-expansion-panels>
                    <v-expansion-panel style="margin-top: 20px;" class="expansion-panel-style">
                      <v-expansion-panel-title style="font-weight: bold;">
                        রোগ প্রতিরোধের উপায়
                      </v-expansion-panel-title>
                      <v-expansion-panel-text style="text-align: justify; font-family: 'Noto Sans Bengali', sans-serif; font-weight: 500; font-size: 18px;">
                        <div v-html="data_fetched.prevention_method"></div>
                      </v-expansion-panel-text>
                    </v-expansion-panel>

                    <v-expansion-panel class="expansion-panel-style">
                      <v-expansion-panel-title style="font-weight: bold;">
                        চিকিৎসা ও ব্যবস্থাপনা
                      </v-expansion-panel-title>
                      <v-expansion-panel-text style="text-align: justify; font-family: 'Noto Sans Bengali', sans-serif; font-size: 18px;">
                        <div v-html="data_fetched.treatment"></div>
                      </v-expansion-panel-text>
                    </v-expansion-panel>

                    <v-expansion-panel class="expansion-panel-style">
                      <v-expansion-panel-title style="font-weight: bold;">
                        রোগের ঝুঁকিপূর্ণ এলাকা
                      </v-expansion-panel-title>
                      <v-expansion-panel-text style="text-align: justify; font-family: 'Noto Sans Bengali', sans-serif; font-size: 18px;">
                        <div v-html="data_fetched.risk_areas"></div>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </div>
              </div>
              <div v-else>
                <p>No data available</p>
              </div>
            </v-sheet>
          </v-col>

        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      links: ["Prediction", "About", "Profile", "Settings"],
      showContent2: false,
      showContent3: false,
      showLoader: false,
      selectedImage: null,
      imagePreview: null,
      responseData: null,
      diseaseName: null,
      valueConfidendce: [],
      data_fetched: "",
      classMapping: {
        0: "Corn Common Rust",
        1: "Corn Gray Leaf Spot",
        2: "Corn Healthy",
        3: "Corn Northern Leaf Blight",
        4: "Potato Early Blight",
        5: "Potato Healthy",
        6: "Potato Late Blight",
        7: "Tomato Bacterial Spot",
        8: "Tomato Early Blight",
        9: "Tomato Late Blight",
        10: "Tomato Leaf Mold",
        11: "Tomato Septoria Leaf Spot",
        12: "Tomato Target Spot",
        13: "Tomato Tomato Yellow Leaf Curl Virus",
        14: "Tomato Tomato Mosaic Virus",
        15: "Tomato Healthy",
        16: "Wheat Brown Rust",
        17: "Wheat Healthy",
        18: "Wheat Yellow Rust",
      },
    };
  },
  methods: {
    async startPrediction() {
      if (!this.selectedImage) return;

      this.imagePreview = URL.createObjectURL(this.selectedImage);
      this.showLoader = true;

      const formData = new FormData();
      formData.append("file", this.selectedImage);

      try {
        // Send the image to the API endpoint
        const response = await fetch("http://localhost:8081/detect", {
          method: "POST",
          body: formData,
        });

        // Check if the response is OK
        if (response.ok) {
          this.responseData = await response.json();
          this.diseaseName = this.classMapping[this.responseData.top_predictions[0].class];

          for (let i = 0; i < this.responseData.top_predictions.length; i++) {
            this.valueConfidendce.push(
              this.responseData.top_predictions[i].confidence_score
            );
          }
        } else {
          console.error("Error:", response.statusText);
        }
        this.fetchData(this.diseaseName);
      } catch (error) {
        console.error("Error:", error);
      } finally {
        // Hide the loader and show the second content
        this.showLoader = false;
        this.showContent2 = true;
        this.showContent3 = true; // Show the third content after prediction
      }
    },

    async fetchData(diseaseName) {
      console.log("Disease Name:", diseaseName);
      const data = {
      disease_name: diseaseName
    };
    try {
      const response = await fetch("http://localhost:8081/fetchData", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)

      });

      if (response.ok) {
        this.data_fetched = await response.json();
        // console.log(this.data_fetched.description); 
    }
    } catch (error) {
      console.error("Error:", error);
    }
  }

,
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}
/* General Content Styles */
.content-sheet {
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  text-align: center;
}

.text-primary {
  color: #1976d2;
}

/* Custom Redesign Styles */
.content-redesign {
  border-radius: 16px;
  padding: 40px 20px;
  border: 1px solid #e0e0e0;
}

.file-input-custom {
  width: 500px;
  margin: 20px auto;
  font-size: 18px;
  font-weight: 500;
  background-color: #ffffff;
  border-radius: 10px;
  border: 1px solid #d6e0f0;
  padding: 16px 24px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  font-family: 'Noto Sans Bengali', sans-serif;
}

.image-preview {
  pointer-events: none;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.predict-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  background-color: #1976d2;
  color: white;
}

.bg-grey-lighten-3 {
  background-color: #f0f4f7;
}

/* Transition Styles */
.slideshow-enter-active,
.slideshow-leave-active {
  transition: all 0.7s ease-in-out;
}

.slideshow-enter,
.slideshow-leave-to {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}

.slideshow-leave-active {
  transform: translateX(-50px) scale(0.9);
}

.label-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.class-name {
  flex: 1;
  font-size: 16px;
}

.bar-container {
  flex: 2;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  width: 300px;
}

.bar-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.prediction-item {
  margin-top: 30px;
}
.expansion-panel-style{
  overflow-x: hidden;
  margin: 0 auto;
  max-width: 800px; 
  margin-top: 10px; 
  box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.1);
}
</style>
