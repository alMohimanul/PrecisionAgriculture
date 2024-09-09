<template>
  <v-app>
    <v-main>
      <PredictionPage/>
    </v-main>
  </v-app>
</template>

<script>
import PredictionPage from './components/PredictionPage.vue'

export default {
  name: 'App',

  components: {
    PredictionPage,
  },

  data: () => ({
    //
  }),
}
</script>
