<template>
  <v-list-item two-line>
    <v-list-item-content class="justify-center">
      <div
        v-for="(player, index) in players"
        v-bind:key="player.name"
        class="player"
      >
        <v-row cols="12" sm="8" class="ma-2">
          <div>
            <v-list-item-title>
              <h2>{{ player.name }}</h2></v-list-item-title
            >

            <v-list-item-subtitle>
              <h3>{{ player.score }}</h3>
            </v-list-item-subtitle>
            <v-row cols="12" sm="8" class="ma-2">
              <div
                v-for="(player) in players"
                v-bind:key="player.name"
                class="player"
              ></div>
            </v-row>
          </div>
          <div
            class="player justify-center"
            style="text-align: center"
            v-if="index == 0"
          >
            <h3 style="color: lightcoral; padding: 10px 0px 0px 0px">
              nextPlayer
            </h3>
          </div>
        </v-row>
      </div>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import ResizeText from "vue-resize-text";

export default {
  name: "PlayerList",
  props: ["players"],
  directives: {
    ResizeText,
  },
  data: function () {
    return {};
  },
  created() {
    this.$root.$refs.PlayerList = this;
    this.$root.$refs.playDart.init();
    //this.init();
    // this.createWebsocket()
  },
  methods: {
    popout(temp_player){ 
      let playersList = this.players;
      let temp1_player = playersList[0];
      if(temp_player.name=playersList[0].name) {
        playersList.shift();
      }
      playersList.push(temp1_player)
      this.players = playersList
    },
  },
};
</script>

<style>
.players {
  display: flex;
  color: white;
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

