

new Vue ({
    el:'#app',
    data: function(){
        return {
            input:'',
            userInfo: {
                name:'',
                gender:'',
                phoneNum:'',
            },
            tableData: [{
                name: '小明',
                gender:'男',
                phoneNum: '18645803579',
              }, {
                name: '李华',
                gender:'女',
                phoneNum: '13345830649',
              },{
                name: 'Tom',
                gender:'男',
                phoneNum: '18245850046',
              }],
              dialogVisible: false,
              editObj: {
                name:'',
                gender:'',
                phoneNum:'',
              },
              userIndex: 0,
        }
    },
    methods: {
        addUser(){
          if(!this.userInfo.name){
            this.$message({
              message: '请输入姓名!',
              type: 'warning'
            });
            return;
          }
          if(!this.userInfo.gender){
            this.$message({
              message: '请输入性别!',
              type: 'warning'
            });
            return;
          }
          if(!this.userInfo.phoneNum){
            this.$message({
              message: '请输入电话号码!',
              type: 'warning'
            });
            return;
          }
          if(!/^1[3456789]\d{9}$/.test(this.userInfo.phoneNum)){
            this.$message({
              message: '请输入正确格式的电话号码!',
              type: 'warning'
            });
            return;
          }
          this.tableData.push(this.userInfo);
          this.userInfo={
            name:'',
            gender:'',
            phoneNum:'',
        };
      },
      delUser(idx) {
        this.$confirm('确认删除？')
          .then(_ => {
            this.tableData.splice(idx,1);
          })
          .catch(_ => {});
      },
      editUser(item, idx) {
        this.userIndex = idx;
        this.editObj = {
          name: item.name,
          gender: item.gender,
          phoneNum: item.phoneNum,
        };
        this.dialogVisible = true;
      },
      handleClose() {
        this.dialogVisible = false;
      },
      confirm(){
        this.dialogVisible = false;
        Vue.set(this.tableData, this.userIndex, this.editObj);
      }
          

    }
})