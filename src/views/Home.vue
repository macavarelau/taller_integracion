<template>
  <div class="home">
    <Navbar
      @search-text="getCharacters"
      @select-char="getCharacter"
      :searchList="charactersSearched"
    />
    <div class="series" v-if="dataLoaded && !characterLoaded">
      <Serie
        @char-select="getCharacter"
        name="Breaking Bad"
        :seasons="bb_seasons"
        :selectedSeason="selectedSeasonBB"
        @season-select="selectSeasonBB"
      />
      <Serie
        @char-select="getCharacter"
        name="Better Call Saul"
        :seasons="bcs_seasons"
        :selectedSeason="selectedSeasonBCS"
        @season-select="selectSeasonBCS"
      />
    </div>
    <div class="character" v-if="characterLoaded">
      <Character
        :character="characterSearched"
        @season-selectedBB="selectSeasonBB"
        @season-selectedBCS="selectSeasonBCS"
        @back="goBack"
      />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Serie from "@/components/Serie.vue";
import Character from "@/components/Character.vue";
import Navbar from "../components/Navbar.vue";
import axios from "axios";

export default {
  name: "Home",
  components: {
    Serie,
    Character,
    Navbar,
  },
  data() {
    return {
      bb_seasons: {},
      bbSeasonsLoaded: false,
      bcs_seasons: {},
      bcsSeasonsLoaded: false,
      bb_episodes: null,
      bcs_espisodes: null,
      bb_characters: null,
      bcs_characters: null,
      characterSearched: null,
      charactersSearched: [],
      selectedSeasonBB: null,
      selectedSeasonBCS: null,
    };
  },
  computed: {
    dataLoaded() {
      if (this.bbSeasonsLoaded && this.bcsSeasonsLoaded) return true;
      else return false;
    },
    characterLoaded() {
      if (this.characterSearched !== null) return true;
      else return false;
    },
  },
  methods: {
    selectSeasonBB(season) {
      let num = parseInt(season);
      this.characterSearched = null;
      this.selectedSeasonBCS = null;
      this.selectedSeasonBB = num;
    },
    selectSeasonBCS(season) {
      let num = parseInt(season);
      this.characterSearched = null;
      this.selectedSeasonBB = null;
      this.selectedSeasonBCS = num;
    },
    getCharacter(character) {
      let url_request =
        "https://tarea-1-breaking-bad.herokuapp.com/api/characters?name=";
      let resp = character.replace(" ", "+");
      url_request = url_request + resp;
      axios
        .get(url_request)
        .then((response) => {
          this.characterSearched = response.data[0];
          console.log(this.characterSearched);
        })
        .catch((error) => {
          console.log(error.response);
        });
    },
    getCharacters(character) {
      let url_request =
        "https://tarea-1-breaking-bad.herokuapp.com/api/characters?name=";
      let resp = character.replace(" ", "+");
      url_request = url_request + resp;
      axios
        .get(url_request)
        .then((response) => {
          this.charactersSearched = response.data;
          console.log(this.charactersSearched);
        })
        .catch((error) => {
          console.log(error.response);
        });
    },
    goBack() {
      this.characterSearched = null;
    },
  },
  created() {
    axios
      .get(
        "https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Breaking+Bad"
      )
      .then((response) => {
        this.bb_episodes = response.data;
        let set = new Set();
        this.bb_episodes.forEach((element) => {
          set.add(element.season);
        });
        this.bb_episodes.forEach((episode) => {
          set.forEach((ss) => {
            if (!(ss in this.bb_seasons)) {
              this.bb_seasons[ss] = [];
            }
            if (episode.season == ss) {
              this.bb_seasons[ss].push(episode);
            }
          });
        });
        this.bbSeasonsLoaded = true;
      })
      .catch((error) => {
        console.log(error.response);
      });
    axios
      .get(
        "https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series=Better+Call+Saul"
      )
      .then((response) => {
        this.bcs_episodes = response.data;
        let set = new Set();
        this.bcs_episodes.forEach((element) => {
          set.add(element.season);
        });
        this.bcs_episodes.forEach((episode) => {
          set.forEach((ss) => {
            if (!(ss in this.bcs_seasons)) {
              this.bcs_seasons[ss] = [];
            }
            if (episode.season == ss) {
              this.bcs_seasons[ss].push(episode);
            }
          });
        });
        this.bcsSeasonsLoaded = true;
      })
      .catch((error) => {
        console.log(error.response);
      });
  },
};
</script>
<style scoped>
.series {
  display: flex;
  align-items: flex-start;
}
</style>
