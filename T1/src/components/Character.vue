<template>
  <div class="main">
    <div class="image">
      <img :src="character.img" alt="" />
    </div>
    <div class="information">
      <p><b>Nombre:</b> {{ character.name }}</p>
      <p><b> Sobrenombre:</b> {{ character.nickname }}</p>
      <p><b> Ocupación:</b></p>
      <div
        v-for="(ocupation, index) in character.occupation"
        v-bind:key="index"
      >
        <li>{{ ocupation }}</li>
      </div>
      <p><b> Estado actual:</b> {{ character.status }}</p>
      <p><b> Participación Breaking Bad:</b></p>
      <div
        class="clickableDiv"
        v-for="(season, index) in character.appearance"
        v-bind:key="index"
        v-on:click="selectSeasonBB(season)"
      >
        Temporada {{ season }}
      </div>
      <p><b>Participación Better Caul Saul:</b></p>
      <div
        class="clickableDiv"
        v-for="(season, index) in character.better_call_saul_appearance"
        v-bind:key="index"
        v-on:click="selectSeasonBCS(season)"
      >
        Temporada {{ season }}
      </div>
      <p><b>Interpretado por:</b> {{ character.portrayed }}</p>
      <p><b>Series:</b> {{ character.category }}</p>
      <!-- <div v-for="(serie, index) in character.category" v-bind:key="index">
        <li>{{ serie }}</li>
      </div> -->
      <div class="buttonBack">
        <b-button type="is-dark" v-on:click="goBack">Atrás</b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Character",
  props: {
    character: Object,
  },
  methods: {
    goBack() {
      this.$emit("back");
    },
    selectSeasonBB(season) {
      console.log("funcione");
      this.$emit("season-selectedBB", season);
    },
    selectSeasonBCS(season) {
      console.log("funcione");
      this.$emit("season-selectedBCS", season);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main {
  display: flex;
  max-width: 60%;
  margin-inline: auto;
  margin-bottom: 100px;
  background-color: #ededed;
  border-radius: 10px 10px 10px 10px;
  margin-top: 3%;
  box-shadow: black;
}

.information {
  display: flex;
  flex-direction: column;
  width: 55%;
  padding: 5%;
  background-color: #ededed;
  border-radius: 10px 10px 10px 10px;
  justify-content: center;
  line-height: 160%;
}

.image {
  width: 45%;
}

img {
  border-radius: 10px 0 0 10px;
}

.buttonBack {
  margin-top: 8%;
}

.clickableDiv:hover {
  font-weight: bolder;
  cursor: pointer;
  color: sienna;
}
</style>
