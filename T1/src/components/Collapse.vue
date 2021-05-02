<template>
  <section>
    <b-collapse
      aria-id="contentIdForA11y2"
      class="panel"
      animation="slide"
      v-model="isOpen"
    >
      <template #trigger>
        <div
          class="panel-heading"
          role="button"
          aria-controls="contentIdForA11y2"
        >
          <strong>{{ "#" + episode.episode + " " + episode.title }}</strong>
        </div>
      </template>
      <div class="panel-block">
        <div class="information">
          <strong>Temporada:</strong> {{ episode.season }} <br />
          <strong>Fecha de lanzamiento:</strong> {{ dateCorrected }} <br />
          <strong>Serie:</strong> {{ episode.series }} <br />
          <strong>Personajes:</strong> <br />
        </div>
        <div class="characters">
          <div
            class="character"
            v-for="(char, index) in episode.characters"
            v-bind:key="index"
            v-on:click="selectChar(char)"
          >
            {{ char }}
          </div>
        </div>
      </div>
    </b-collapse>
  </section>
</template>

<script>
export default {
  name: "Collapse",
  props: {
    episode: Object,
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    dateCorrected() {
      let month = new Array();
      month[0] = "Enero";
      month[1] = "Febrero";
      month[2] = "Marzo";
      month[3] = "Abril";
      month[4] = "Mayo";
      month[5] = "Junio";
      month[6] = "Julio";
      month[7] = "Agosto";
      month[8] = "Septiembre";
      month[9] = "Octubre";
      month[10] = "Noviembre";
      month[11] = "Deciembre";
      let fecha = new Date(this.episode.air_date);
      let day = fecha.getDate() + 1;
      let mes = month[fecha.getMonth()];
      let year = fecha.getFullYear();
      return day + " de " + mes + " del " + year;
    },
  },
  methods: {
    selectChar(char) {
      this.$emit("char-select", char);
    },
  },
};
</script>
<style scoped>
.collapse {
  width: 85%;
  margin: auto;
}
.panel-block {
  display: flex;
  flex-direction: column;
}
.characters {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}
.character {
  margin-inline: 1%;
}
.character:hover {
  font-weight: bolder;
  cursor: pointer;
  color: sienna;
}
</style>
