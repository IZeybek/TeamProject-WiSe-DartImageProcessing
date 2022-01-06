<template>
  <div>
    <div
      v-for="(item, index) in dartScores"
      v-bind:key="index"
      :style="{ padding: '5px', 'background-color': getTurn(index) }"
    >
      <v-row cols="1" sm="8" class="ma-2">
        <div class="justify-center">
          <img
            src="../assets/dart.png"
            width="30"
            height="30"
            style="padding: 2px"
          />
        </div>
        <div
          v-if="item.score == 0"
          style="padding-left: 10px; margin-top: 2px; font-size: 20px"
        >
          <v-icon>mdi-equal</v-icon>{{ item.score }}
        </div>
        <div v-else style="padding-left: 8px">
          <v-icon>mdi-equal</v-icon>
        </div>
      </v-row>
      <v-divider></v-divider>
    </div>
  </div>
</template>

<script>
export default {
  name: "DartScorer",
  props: ["dartScores"],
  data: function () {
    return {};
  },
  methods: {
    getTurn(index) {
      if (this.dartScores[index].score == 0) {
        return "lightgreen";
      } else {
        return "tranparent";
      }
    },
  },
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

