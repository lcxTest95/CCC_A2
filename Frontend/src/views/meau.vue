
<template>
    <div class="layout">
        <Layout>
            <Header :style="{position: 'fixed', width: '100%'}" style="z-index:9999">
                <Menu mode="horizontal" theme="dark" active-name="1">
                    <!-- 替换为logo -->
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <MenuItem name="1" to="/secondPage">
                            <Icon type="ios-home" /></Icon>
                           Home
                        </MenuItem>
                        <MenuItem name="2" to="/map">
                            <Icon type="ios-map" /></Icon>
                            Map
                        </MenuItem>
                        <MenuItem name="3" to="/third">
                            <Icon type="ios-analytics"></Icon>
                            Graphs
                        </MenuItem>
                        <MenuItem name="4" to="/fourth">
                            <Icon type="ios-paper"></Icon>
                            Fourth Page
                        </MenuItem>
                    </div>
                    
                </Menu>
            </Header>
            <Content :style="{margin: '88px 20px 0', background: '#fff', minHeight: '83.8vh'}">
                <router-view></router-view>
            </Content>
            <Footer class="layout-footer-center">2011-2016 &copy; TalkingData</Footer>
        </Layout>
    </div>
</template>
<script>
    export default {
        
    }
</script>
<style scoped>
    .layout{
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: hidden;
    }
    .layout-logo{
        width: 100px;
        height: 30px;
        background: #5b6270;
        color: #fff;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 15px;
        left: 20px;
    }
    .layout-nav{
        width: 800px;
        margin: 0 auto;
        margin-left: 20px;
    }
    .layout-footer-center{
        text-align: center;
    }
</style>
