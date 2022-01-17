<template>
  <div class="v-main__wrap">
    <div class="container">
      <div class="row">
        <div class="col-sm-2 col-12">
          <div
            class="v-sheet theme--light rounded-lg"
            style="min-height: 268px"
          >
            <player-list :players="players"></player-list>
          </div>
        </div>
        <div class="col-sm-8 col-12">
          <div class="v-sheet theme--light rounded-lg" style="min-height: 50vh">
            <div class="ma-2 d-flex overflow-auto justify-center">
              <v-col cols="12" sm="8" class="ma-2 justify-center">
                <div v-if="win">
                  <win :currentPlayer="currentPlayer"></win>
                </div>
                <div v-else>
                  <current-player :currentPlayer="currentPlayer"></current-player>
                  </div>
                <!--current-player :currentPlayer="currentPlayer"></current-player-->
                <div class="nextPlayer">
                  <v-btn @click="callibration()" small dark>Calibration</v-btn>
                </div>
              </v-col>
            </div>
          </div>
        </div>
        <div class="col-sm-2 col-12">
          <div class="v-sheet theme--light rounded-lg"
            style="min-height: 268px">
          <dart-scorer :dartScores="dartScores"></dart-scorer>
          <div class="justify-center" style ="text-align:center">
            <v-btn style ="" v-show="!win" @click="changePlayer()" small dark>done?</v-btn>
            <v-btn v-show="win" @click="init()" small dark>New Game?</v-btn>
          </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ResizeText from "vue-resize-text";
import PlayerList from "./PlayerList.vue";
import CurrentPlayer from "./CurrentPlayer.vue";
import DartScorer from "./DartScorer.vue";
import Win from "./Win.vue"

export default {
  name: "playDart",
  props: ["playernames", "initialSconre"],
  components: { PlayerList, CurrentPlayer, DartScorer, Win },
  directives: {
    ResizeText,
  },
  data: function () {
    return {
      record: [],
      win: false,
      serverscore: 0,
      isHidden: false,
      players: [],
      correct: "",
      playerCount: 0,
      websocket:null,
      pointsweb:[],
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
    this.currentPlayer = this.players[0]
    let temp_player=this.players.shift()
    this.players.push(temp_player)
    this.createWebSocket()
    setTimeout(() => { this.websocket.send(JSON.stringify({
        "request": "10"
        })) }, 2000);
  },
  methods: {
    changePlayer() {
      //this.$root.$refs.PlayerList.popout(this.currentPlayer);
      let finalscore = this.$root.$refs.DartScorer.getScore_all_tries_together();
      this.calculateScore(finalscore)
      if(this.win) {
        console.log("test")
      } else {
        this.currentPlayer = this.players[0];
        let temp_player = this.currentPlayer
        this.$root.$refs.PlayerList.popout(temp_player);
      }
      //this.playerCount = (this.playerCount + 4) % this.players.length;
      //this.currentPlayer = this.players[0];
      //let temp_player = this.currentPlayer
      //this.$root.$refs.PlayerList.popout(temp_player);
    },

    init() {
      const darts = [];
      for (let i = 0; i < 3; i++) {
        darts.push({score:0,}); // some changes for testing
        // if (i == 0) {
        //   darts.push({
        //     score: 5,
        //   });
        // } else {
        //   darts.push({
        //     score: -1,
        //   });
        // }
      }
      this.dartScores = darts;
      this.win=false;
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
    calculateScore(finalscore){
      let tmp_score = this.currentPlayer.score;
      tmp_score = tmp_score - finalscore;
      if(tmp_score > 0) {
        this.currentPlayer.score = tmp_score
      } else if(tmp_score == 0) {
        this.currentPlayer.score = tmp_score
        this.win = true;
      } else {
        alert("try again")
      }
    },
    createWebSocket() {
      this.websocket = new WebSocket("ws://127.0.0.1:9000")
      this.websocket.onopen =()=>{
        console.log("Connected to Backend")
      }
      this.websocket.onclose = function() {
        console.log("connection with websocket closed")
      }
      this.websocket.onerror =function(error) {
        console.log(error)
        console.log("WebSocket is closed now."+error);
      }
      this.websocket.onmessage = function (e) {
        let number = JSON.parse(e.data).value
        const darts = [];
        console.log(number)
        // if(typeof e.data ==="string") {
        //   let json = JSON.parse(e.data);
        // }
      }
    },
    callibration(){
      console.log(this.serverscore)
    }
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

