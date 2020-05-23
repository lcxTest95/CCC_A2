
<template>
    <div class="layout">
        <Layout>
            <Header :style="{position: 'fixed', width: '100%'}" style="z-index:9999">
                <Menu mode="horizontal" theme="dark" active-name="1">
                    <div class="layout-logo"> 
						<img
						src="../assets/images/logo2.png"
						alt
						/>
                        </div>
                    <div class="layout-nav">
                        <MenuItem name="1" to="/">
                            <Icon type="ios-home" />
							Home Page
                        </MenuItem>
                        <MenuItem name="2" to="/map">
                            <Icon type="ios-map" />
                            Heat Map
                        </MenuItem>
                        <MenuItem name="3" to="/graphs">
                            <Icon type="ios-analytics" />
							Statistical Graph
                        </MenuItem>
                        <MenuItem name="4" to="/report">
                            <Icon type="ios-paper"/>
                            Modelling Report
                        </MenuItem>
                    </div>
                </Menu>
            </Header>
            <Content :style="{margin: '90px 20px 0', background: '#fff', minHeight: '80vh'}">
                <router-view></router-view>
            </Content>
            <Footer class="layout-footer-center">2020 S1 COMP90024 Team 36</Footer>
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
        background: #52596d;
        color: #fff;
        border-radius: 3px;
        float: left;
        position: relative;
        top: 10px;
        left: 0px;
    }
	.layout-logo img {
	  width: 120px;
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
