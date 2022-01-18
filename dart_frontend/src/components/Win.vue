<template>
  <div class="v-sheet theme--light rounded-lg" style="min-height: 268px">
    <div class="score">
      <v-list-item-title>
        <h2>{{ currentPlayer.name }}</h2></v-list-item-title
      >
      <v-list-item-subtitle>
        <h3>{{currentPlayer.score}}</h3>
      </v-list-item-subtitle>
      <div
        class="scorePoint"
        v-resize-text="{
          ratio: 0.3,
          minFontSize: '16px',
          maxFontSize: '400px',
        }"
      >
        win
      </div>
    </div>
  </div>
</template>

<script>
import ResizeText from "vue-resize-text";

export default {
  name: "CurrentPlayer",
  props: ["currentPlayer"],
  directives: {
    ResizeText,
  },
  data: function () {
    return {};
  },
  methods: {},
};
</script>


<style>
#shootout {
  display: relative;
}
.head {
  display: grid;
  grid-template-columns: 2fr 1fr;
  place-items: center;
  /*border: 5px solid black;*/
}

.players {
  display: flex;
  color: white;
}
.record {
  background-color: #333;
}
h1 {
  background-color: lightblue;
  text-align: center;
}
h2 {
  padding: 10px 0px 0px 0px;
}
h3 {
  color: lightblue;
}
.record > div {
  color: white;
  font-weight: bold;
  font-size: 1rem;
  border: 2px solid white;
  padding: 10px;
  min-width: 150px;
  min-height: 45px;
}
.players > div {
  padding: 10px;
  border-left: 4px solid black;
  border-bottom: 4px solid black;
}
.players > div:last-child {
  border-right: 4px solid black;
}
h3 {
  margin: 0 0 5px 0;
}
.score {
  background-color: #333;
  border-radius: 5px;
  text-align: center;
  color: #fff;
}

.nextPlayer {
  padding-top: 20px;
  text-align: center;
}

.scorePoint {
  font-size: 300px;
  text-align: center;
  color: lightgreen;
}
.player {
  background-color: #333;
  flex-grow: 1;
  padding: 1px 0px 0px 14px;
  color: #fff;
  border-radius: 5px;
}
</style>

