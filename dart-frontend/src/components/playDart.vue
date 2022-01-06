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
              </v-list-item-content>
            </v-list-item>
          </div>
        </div>
        <div class="col-sm-8 col-12">
          <div class="v-sheet theme--light rounded-lg" style="min-height: 70vh">
            <div id="shootout">
              <div class="ma-2 d-flex overflow-auto justify-center">
                 <v-col cols="12" sm="8" class="ma-2">
                   <div >
                     <h1>Welcome to Dart!</h1>
                   </div>
                   <div>
                     <h2>current player:</h2>
                     <h3>{{currentPlayer.name}}</h3>
                   </div>
                  <div  class="score">
                     <h2>PlayerScore:</h2>
                     <p>{{currentPlayer.score}}</p>
                   </div>
                   <v-btn class="justify-center" @click="changePlayer()" small dark
                  >next player</v-btn>
                </v-col>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-2 col-12">
          <div
            class="v-sheet theme--light rounded-lg"
            style="min-height: 268px"
          >
            <div class="head">
              <div class="record">
                <v-btn
                  @click="
                    isHidden = true;
                    debug();
                  "
                >
                  Correction</v-btn
                >
                <input
                  v-if="isHidden"
                  v-model="correct"
                  placeholder="Richtige zahl eingeben"
                />
                <div
                  @click="
                    undo(correct);
                    isHidden = false;
                  "
                >
                  {{ record[0] | totext }}
                </div>
                <div
                  @click="
                    undo();
                    isHidden = true;
                  "
                >
                  {{ record[1] | totext }}
                </div>
                <div
                  @click="
                    undo();
                    isHidden = true;
                  "
                >
                  {{ record[2] | totext }}
                </div>
                <v-btn
                  @click="
                    isHidden = true;
                    debug();
                  "
                  >Failed</v-btn
                >
                <v-btn class="justify-center" @click="startGame()" small dark
                  >Calibration</v-btn
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "playDart",
  props: ["playernames", "initialSconre"],
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
        name: 'player.name',
        score: 301,
        throws: [],
      }
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
    changePlayer() {
      this.playerCount =  (this.playerCount + 1 ) %this.players.length;
      this.currentPlayer = this.players[this.playerCount]
    },

    init() {
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
  border: 5px solid black;
}

.players {
  display: flex;
  color: white;
}
.record {
  justify-self: end;
  background-color: rgb(173, 28, 28);
}
h1 {
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
  margin-right: 10px;
}
.score p {
  font-size: 300px;
  text-align: center;
  background-color: #333;
  border-radius: 5px;
  color: #fff;
}
.player {
  background-color: #333;
  flex-grow: 1;
  padding: 1px 0px 0px 14px;
  color: #fff;
  border-radius: 5px;
}
.player.active:nth-child(1) {
  background-color: red;
}
.player.active:nth-child(2) {
  background-color: blue;
}
.player.active:nth-child(3) {
  background-color: green;
}
.player.active:nth-child(4) {
  background-color: purple;
}
.player.active:nth-child(5) {
  background-color: rgb(28, 114, 110);
}

.playerchange,
.gameover {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  font-weight: bold;
  transform: translate(-50%, -50%);
  background-color: rgb(189, 201, 87);
  color: white;
  font-size: 2rem;
  padding: 30px;
  cursor: pointer;
}
.gameover {
  padding: 0;
}
.gameover > div {
  padding: 30px;
}
.playagain {
  background-color: rgb(45, 102, 19);
}
</style>

