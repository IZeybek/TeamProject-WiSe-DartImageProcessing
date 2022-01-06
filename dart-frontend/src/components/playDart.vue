<template>
  <div class="v-main__wrap">
    <div class="container">
      <div class="row">
        <div class="col-sm-2 col-12">
          <div
            class="v-sheet theme--light rounded-lg"
            style="min-height: 268px"
          >
            <v-list-item two-line>
              <v-list-item-content class="justify-center">
                <div
                  v-for="(player, index) in players"
                  v-bind:key="player.name"
                  :class="{ active: turn === index, player }"
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
                          v-for="(player, index) in players"
                          v-bind:key="player.name"
                          :class="{ active: turn === index, player }"
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
          </div>
        </div>
        <div class="col-sm-8 col-12">
          <div class="v-sheet theme--light rounded-lg" style="min-height: 50vh">
            <div class="ma-2 d-flex overflow-auto justify-center">
              <v-col cols="12" sm="8" class="ma-2 justify-center">
                <div class="score">
                  <v-list-item-title>
                    <h2>{{ currentPlayer.name }}'s</h2></v-list-item-title
                  >
                  <v-list-item-subtitle>
                    <h3>Score</h3>
                  </v-list-item-subtitle>
                  <div
                    class="scorePoint"
                    v-resize-text="{
                      ratio: 0.3,
                      minFontSize: '16px',
                      maxFontSize: '400px',
                    }"
                  >
                    {{ currentPlayer.score }}
                  </div>
                </div>
                <div class="nextPlayer">
                  <v-btn @click="changePlayer()" small dark>next player</v-btn>
                </div>
              </v-col>
            </div>
          </div>
        </div>
        <div class="col-sm-2 col-12">
          <div
            class="v-sheet theme--light rounded-lg"
            style="min-height: 268px"
          >
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
            <div class="head justify-center">
              <v-btn @click="changePlayer()" small dark>done?</v-btn>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ResizeText from "vue-resize-text";

export default {
  name: "playDart",
  props: ["playernames", "initialSconre"],
  directives: {
    ResizeText,
  },
  data: function () {
    return {
      record: [],
      serverscore: 0,
      isHidden: false,
      players: [],
      correct: "",
      playerCount: 0,
      connection: null,
      currentPlayer: {
        name: "player.name",
        score: 301,
        throws: [],
      },
      dartScores: [],
    };
  },
  filters: {
    totext(serverscore) {
      if (serverscore == 0) {
        return "";
      }
      if (serverscore == 0) {
        return serverscore;
      }
    },
  },
  created() {
    this.init();
    // this.createWebsocket()
  },
  methods: {
    getTurn(index) {
      if (this.dartScores[index].score == 0) {
        return "lightgreen";
      } else {
        return "tranparent";
      }
    },
    changePlayer() {
      this.playerCount = (this.playerCount + 1) % this.players.length;
      this.currentPlayer = this.players[this.playerCount];
    },

    init() {
      const darts = [];
      for (let i = 0; i < 3; i++) {
        if (i == 0) {
          darts.push({
            score: 0,
          });
        } else {
          darts.push({
            score: -1,
          });
        }
      }
      this.dartScores = darts;
      this.players = this.playernames.map((player) => ({
        name: player.name,
        score: this.initialScore || 301,
        throws: [],
      }));
    },
    debug() {
      console.log(this.isHidden);
    },
    undo(correct) {
      // implement later
      console.log("life is good " + correct);
    },
    createWebsocket() {
      this.connection = new WebSocket("ws://127.0.0.1:6969");
      console.log(this.connection);
      this.connection.send("hello");
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

