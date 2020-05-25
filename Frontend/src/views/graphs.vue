
<template>
  <div class="graphs">
    <div>
      <div style="width:900px;height:350px;margin-top:30px;">
        <el-transfer
          style="text-align: left; display: inline-block;height:400px;"
          v-model="value"
          filterable
          :render-content="renderFunc"
          :titles="['Source', 'Target']"
          :button-texts="['Delete', 'Add']"
          :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
      }"
          @change="handleChange"
          :data="legendData"
        ></el-transfer>
      </div>
      <div
        id="inc_edu"
        style="width:800px;height:400px;margin-top:30px;margin-left:70px;position:relative;left:0px;"
      ></div>
    </div>
    <div style="width:50%;margin-right:30px;margin-top:20px;">
      <div id="income" style="width:700px;height:400px;float:right"></div>
      <div id="education" style="width:700px;height:400px;float:right"></div>
    </div>
  </div>
</template>
<script>
import axios from "@/assets/axios.js";
export default {
  data() {
    return {
      all_data: [],
      selected: {},
      legendData: [],
      value: [66, 50, 73, 47, 23],
      renderFunc(h, option) {
        return h("span", {}, option.label);
      }
    };
  },
  mounted() {
    this.data_process();
  },
  methods: {
    handleChange(value, direction, movedKeys) {
      if (this.value.length > 5) {
        alert("Exceed the maximum value of 5, please choose again!");
        for (var i = this.value.length - 1; i >= 0; i--) {
          let a = this.value[i];
          for (var j = movedKeys.length - 1; j >= 0; j--) {
            let b = movedKeys[j];
            if (a == b) {
              this.value.splice(i, 1);
              movedKeys.splice(j, 1);
              break;
            }
          }
        }
      }
      this.draw_inc();
      this.draw_edu();
      this.draw_inc_edu();
    },
     data_process() {
      //Get data from Back-end
	  let LatLon = require("../assets/json/SA4_2016_AUST.json");
      axios({
        method: "GET",
        url: "http://172.26.132.19:5000/admin"
      }).then(res => {
        let test_data = res.data;
        let data = [];
        let count_LatLon = 0;
        for (var key1 in LatLon["features"]) {
          count_LatLon++;
          let name_value = LatLon["features"][key1]["properties"]["SA4_CODE"];
          let name_value1 =
            LatLon["features"][key1]["properties"]["STATE_NAME"];
          LatLon["features"][key1]["properties"]["name"] = name_value;
          if (test_data[name_value]) {
            let json = {
              name: LatLon["features"][key1]["properties"]["SA4_NAME"],
              inc: test_data[name_value]["inc"],
              edu: test_data[name_value]["edu"]
            };
            data.push(json);
            if (this.legendData.length < 89) {
              this.legendData.push({
                disabled: false,
                key: Number(key1),
                label: LatLon["features"][key1]["properties"]["SA4_NAME"]
              });
            }
          }
        }
        this.all_data = data;
        this.draw_inc();
        this.draw_edu();
        this.draw_inc_edu();
      });
    },
    //Income Pie Chart
    draw_inc() {
      var data_list = [];
      var name_list = [];
      for (var i = 0; i < this.value.length; i++) {
        data_list.push({
          name: this.all_data[this.value[i]].name,
          value: this.all_data[this.value[i]].inc
        });
        name_list.push(this.all_data[this.value[i]].name);
      }
      var myChart = this.$echarts.init(document.getElementById("income"));
      var option = {
        title: {
          text: "Median Income per Employed Person",
          left: "center",
          top: "20px"
        },
        tooltip: {
          trigger: "item",
          formatter: "{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "right",

          data: name_list
        },
        series: [
          {
            name: "Visit Source",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: data_list,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
    // Education Pie Chart
    draw_edu() {
      var data_list = [];
      var name_list = [];
      for (var i = 0; i < this.value.length; i++) {
        data_list.push({
          name: this.all_data[this.value[i]].name,
          value: this.all_data[this.value[i]].edu
        });
        name_list.push(this.all_data[this.value[i]].name);
      }
      var myChart = this.$echarts.init(document.getElementById("education"));
      var option = {
        title: {
          text: "Aged 15 Years &" + '\n' + "Over Completed Year 9 Or Equivalent",
          left: "center",
          top: "20px"
        },
        tooltip: {
          trigger: "item",
          formatter: "{b} : {c} ({d}%)"
        },
        legend: {
          orient: "vertical",
          left: "right",
          data: name_list
        },
        series: [
          {
            name: "Visit Source",
            type: "pie",
            radius: "55%",
            center: ["50%", "60%"],
            data: data_list,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    },
	// Income and Education Bar Chart
    draw_inc_edu() {
      var data_list = [[], []];
      var name_list = [];
      for (var i = 0; i < this.value.length; i++) {
        data_list[0].push(this.all_data[this.value[i]].inc);
        data_list[1].push(this.all_data[this.value[i]].edu);
        name_list.push(this.all_data[this.value[i]].name);
      }
      var myChart = this.$echarts.init(document.getElementById("inc_edu"));
      var option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            crossStyle: {
              color: "#999"
            }
          }
        },
        toolbox: {
          feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ["line", "bar"] },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        legend: {
          data: ["Income", "Education"]
        },
        xAxis: [
          {
            type: "category",
            data: name_list,
            axisPointer: {
              type: "shadow"
            },
            axisLabel: {
              interval: 0,
              rotate: 20
            }
          }
        ],
        yAxis: [
          {
            type: "value",
            name: "Income ($)",
            min: 0,
            max: 72000,
            interval: 6000,
            axisLabel: {
              formatter: "{value}"
            }
          },
          {
            type: "value",
            name: "Education level (%)",
            min: 0,
            max: 12,
            interval: 1,
            axisLabel: {
              formatter: "{value} "
            }
          }
        ],
        series: [
          {
            name: "Income",
            type: "bar",
            barWidth: 30,
            data: data_list[0]
          },
          {
            name: "Education",
            type: "bar",
            barWidth: 30,
            yAxisIndex: 1,
            data: data_list[1]
          }
        ]
      };
      myChart.setOption(option);
    }
  }
};
</script>
<!--size of each chart-->
<style scoped>
.graphs {
  display: flex;
  justify-content: space-between;
  min-width: 1700px;
  max-width: 99vw;
}
.graphs /deep/ .el-transfer-panel {
  width: 200px;
  height: 350px;
}
.graphs /deep/ .el-transfer-panel__list.is-filterable {
  height: 400px;
}
.graphs /deep/ .el-checkbox-group ::-webkit-scrollbar-thumb {
  background-color: #a1a3a9;
  border-radius: 3px;
}
</style>
