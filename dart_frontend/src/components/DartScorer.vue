<template>
  <div>
    <div
      v-for="(item, index) in dartScores"
      v-bind:key="index"
      :style="{ padding: '5px', 'background-color': getTurn(index) }"
      @mouseover="item.showPencil = true"
      @mouseleave="item.showPencil = false"
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
          v-if="isNumeric(item.score)"
          style="padding-left: 10px; margin-top: 2px; font-size: 20px"
        >
          <v-icon>mdi-equal</v-icon>{{ item.score }}
        </div>
        <div v-else style="padding-left: 8px">
          <v-icon>mdi-equal</v-icon> {{ item.score }}
          <!-- change later-->
        </div>
        <!--div @mouseover="showPencil = true"  @mouseleave="showPencil = false"-->
        <img
          v-show="item.showPencil"
          @click="deleteScore(index)"
          @dblclick="item.showInput = false"
          src="../assets/close.png"
          width="30"
          height="30"
          style="padding: 2px; margin-left: 38px"
        />
        <img
          v-show="item.showPencil"
          @click="item.showInput = true"
          @dblclick="item.showInput = false"
          src="../assets/pencil.png"
          width="30"
          height="30"
          style="padding: 2px; margin-left: 38px"
        />
      </v-row>
      <v-text-field
        v-show="item.showInput"
        type="number"
        class="mt-n6"
        v-model.number="corrected"
        placeholder="enter text"
        v-on:keyup.enter="onEnter(index)"
      ></v-text-field>
      

      <v-divider></v-divider>
    </div>
    <div class="justify-center" style="text-align: center">
    <v-btn
                style="margin: 5px"
                small
                dark
                >{{reversedMessage}}</v-btn
                >
    </div>
  </div>
</template>

<script>
import getRound,{setRound} from "../assets/data/gameState";
export default {
  name: "DartScorer",
  props: ["dartScores", "websocket"],
  data: function () {
    return {
      showPencil: false,
      showInput: false,
      corrected: 0,
      interim_score:0,
      roundOffset: 0,
    };
  },
  computed: {
    reversedMessage: function () {
      this.interim_score = 0;
      for(var i = 0; i<3;i++) {
        this.interim_score+=this.dartScores[i].score
      }
      return this.interim_score
    }
  },
  created() {
    this.$root.$refs.DartScorer = this;
    this.dartScores.forEach((item) => {
      this.$set(item, "showPencil", false);
      this.$set(item, "showInput", false);
    });
    this.roundOffset = 0;
    console.log(this.dartScores);
  },
  methods: {
    deleteScore(index) {
      console.log("vor "+ this.roundOffset)
      console.log("vor "+ getRound())
      this.dartScores[index].score = 0;
      setRound(index + 1);
      this.websocket.send(
        JSON.stringify({
          request: 10,
        })
      );
      this.roundOffset += 1;
      console.log("nach "+ this.roundOffset)
      console.log("nach "+ getRound())
    },
    berechnen(score) {
      this.abc+=score
    },
    getTurn(index) {
      if (getRound() == 0) {
        this.$roundOffset = 0;
      }
      if (this.dartScores[index].score == 0) {
        if (getRound() + this.roundOffset == index) {
          return "yellow";
        }
        return "lightgray";
      } else {
        return "lightgreen";
      }
    },
    onEnter: function (index) {
      this.dartScores[index].showInput = false;
      this.dartScores[index].score = this.corrected;
    },
    isNumeric(value) {
      return Number.isInteger(value);
    },
    getDebug() {
      for (let i = 0; i < this.dartScores.length; i++) {
        console.log(this.dartScores[i].score);
      }
    },
    getScore_all_tries_together() {
      let finaladditonScore = 0;
      for (let i = 0; i < this.dartScores.length; i++) {
        finaladditonScore = finaladditonScore + this.dartScores[i].score;
      }
      // for(let i= 0;i<this.dartScores.length;i++) {
      //   this.dartScores[i].score = 0
      // }    for later implementation
      return finaladditonScore;
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

