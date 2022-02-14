<template>
  <v-container>
    <!--- --->
    <v-row>
      <v-col cols="12" sm="12">
        <v-card-actions v-if="game == 0" class="justify-center">
          <v-sheet class="mt-10" rounded="lg" max-width="300" min-height="350">
            <div class="px-4 py-4" style="margin-top: 20px">
              <div  class=".justify-start">
                  
                  <v-card-actions class="justify-center" max-width="250">
                  <v-text-field
                    class="mt-n6"
                    v-model="score"
                    label="max_score"
                    outlined
                    style="margin-top: 20px"
                  ></v-text-field>
                  
                </v-card-actions>
                  
                  <v-card-actions
                  class="justify-center"
                  max-width="250"
                >
                  <v-text-field
                  
                    class="mt-n6"
                    v-model="player_count"
                    label="how many players?"
                    outlined
                    hide-details
                  ></v-text-field>
                  </v-card-actions>
                  <v-divider></v-divider>
                <v-card-actions
                  v-for="(item, index) in reversedMessage"
                  :key="index"
                  class="justify-center"
                  max-width="250"
                >
                  <v-text-field
                    v-model="item.name"
                    label="enter playerName"
                    outlined
                    hide-details
                  ></v-text-field>
                </v-card-actions>
                
                <v-card-actions class="justify-center">
                  <v-btn
                    class="justify-center"
                    @click="startGame()"
                    width="250"
                    height="40"
                    small
                    dark
                  >
                    start new game</v-btn
                  >
                </v-card-actions>
              </div>
              
              <!--  -->
            </div>
            
          </v-sheet>
        </v-card-actions>
        <playDart
                v-if="game == 1"
                v-bind:playernames="players"
                :initialScore="score"
                :websocket ="websocket"
                v-on:gameover="reset"
              />
      </v-col>
      
          
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import playDart from "./playDart.vue";
import "../assets/global.css";

export default Vue.extend({
  name: "StartGame",
  components: {
    playDart,
  },
  created(){
    //this.createWebSocket()
    // setTimeout(() => { this.websocket.send(JSON.stringify({
    //     "request": "10"
    //     })) }, 2000);
  },
  data: () => ({
    player_count: 2,
    game: 0,
    players: [],
    gamestarted: false,
    score: 301,
    websocket:null,
  }),
    computed: {
    reversedMessage: function () {
      return this.getCount(this.player_count)
    }
  },
  methods: {
    reset() {
      this.game = 0;
      this.players = 0;
      this.gamestarted = false;
    },
    getCount(playercount) {
      const players = [];
      for (let i = 0; i < playercount; i++) {
        players.push({ name: "player" + (i + 1) });
      }
      this.players = players;
      return players;
    },
    startGame() {
        this.game = 1;
    },
    log(name){
      console.log(name)
    },
    

  },
});
</script>


<style scoped>
.gamemode,
.playercount > div,
.startgame {
  color: white;
  font-weight: bold;
  padding: 20px 30px;
  cursor: pointer;
}
.score1 {
  background-color: #e40066;
}
.score2 {
  background-color: #03cea4;
}
.playercount > div:nth-child(1) {
  background-color: #fb4d3d;
}
.playercount > div:nth-child(2) {
  background-color: #03cea4;
}

.line {
  display: flex;
  font-weight: bold;
  padding: 10px;
}
.line:nth-child(even) {
  background-color: #f0f0f0;
}
.name {
  color: #333;
}
.score {
  color: rgb(45, 121, 45);
  margin-left: auto;
}
.playernames {
  display: flex;
  flex-direction: column;
  padding: 30px;
  gap: 20px;
}
.playernames > input {
  max-width: 300px;
}
.startgame {
  background-color: #345995;
}
</style>
