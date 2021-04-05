<template>
  <div class="mainDiv">
    <div v-if="name == 'Breaking Bad'" class="mainImage">
      <img
        src="https://staticuestudio.blob.core.windows.net/buhomag/2018/01/22155623/breaking-bad.jpg"
      />
    </div>
    <div v-else class="mainImage">
      <img
        src="https://blogderadiaciones.files.wordpress.com/2018/09/better-call-saul.jpg"
      />
    </div>
    <div class="buttons">
      <div
        class="buttonDiv"
        v-for="(season, index) in seasons"
        v-bind:key="index"
        v-on:click="selectSeason(index)"
      >
        <b-button v-if="!(index == selectedSeason)"
          >Temporada {{ index }}</b-button
        >
        <b-button type="is-dark" v-if="index == selectedSeason"
          >Temporada {{ index }}</b-button
        >
      </div>
    </div>

    <div class="episodes">
      <Collapse
        v-for="(capitulo, index) in seasons[selectedSeason]"
        v-bind:key="index"
        :episode="capitulo"
        @char-select="selectChar"
      />
    </div>
  </div>
</template>

<script>
import Collapse from "../components/Collapse.vue";
export default {
  name: "Serie",
  components: {
    Collapse,
  },
  props: {
    seasons: Object,
    name: String,
    selectedSeason: Number,
  },
  methods: {
    selectSeason(number) {
      if (number == this.selectedSeason) {
        this.$emit("season-select", null);
      } else {
        this.$emit("season-select", number);
      }
    },
    selectChar(char) {
      this.$emit("char-select", char);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.mainDiv {
  margin-top: 3%;
}
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
.buttons {
  margin-top: 2%;
  display: flex;
  justify-content: center;
}
.buttonDiv .button:focus:not(:active),
.button.is-focused:not(:active) {
  -webkit-box-shadow: 0 0 0 0.125em rgb(255, 255, 255);
  box-shadow: 0 0 0 0.125em rgb(255, 255, 255);
  border-color: #dbdbdb;
}
.buttonDiv {
  margin-inline: 5px;
}
.episodes {
  width: 60%;
  margin: auto;
  margin-bottom: 5%;
}

.mainImage {
  width: 50%;
  margin-top: 50%;
  margin: auto;
  border-radius: 10px 10px 10px 10px;
}

.mainImage img {
  border-radius: 10px 10px 10px 10px;
}
</style>
