<template>
    <div class="biz-tab-header">
        <div class="tab-wrapper bk-badge-wrapper">
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetDeployment' }]" @click="toggleRouter('k8sTemplatesetDeployment')">
                Deployment
                <span class="bk-badge">{{deployments.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetService' }]" @click="toggleRouter('k8sTemplatesetService')">
                Service
                <span class="bk-badge">{{services.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetConfigmap' }]" @click="toggleRouter('k8sTemplatesetConfigmap')">
                ConfigMap
                <span class="bk-badge">{{configmaps.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetSecret' }]" @click="toggleRouter('k8sTemplatesetSecret')">
                Secret
                <span class="bk-badge">{{secrets.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetDaemonset' }]" @click="toggleRouter('k8sTemplatesetDaemonset')">
                DaemonSet
                <span class="bk-badge">{{daemonsets.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetJob' }]" @click="toggleRouter('k8sTemplatesetJob')">
                Job
                <span class="bk-badge">{{jobs.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetStatefulset' }]" @click="toggleRouter('k8sTemplatesetStatefulset')">
                StatefulSet
                <span class="bk-badge">{{statefulsets.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetIngress' }]" @click="toggleRouter('k8sTemplatesetIngress')">
                Ingress
                <span class="bk-badge">{{ingresss.length}}</span>
            </div>
            <div :class="['header-item', { 'active': activeRoute === 'k8sTemplatesetHPA' }]" @click="toggleRouter('k8sTemplatesetHPA')">
                HPA
                <span class="bk-badge">{{HPAs.length}}</span>
            </div>
        </div>
        <div :class="['biz-var-panel', { 'show': isVarPanelShow }]" v-clickoutside="hidePanel">
            <div class="var-panel-header">
                <bcs-popover :content="isVarPanelShow ? $t('关闭') : $t('查看可用变量')" placement="left" v-if="!isVarPanelShow">
                    <button class="var-panel-trigger" @click.stop.prevent="togglePanel">
                        <i class="bcs-icon bcs-icon-angle-left"></i>
                    </button>
                </bcs-popover>
                <button class="var-panel-trigger" @click.stop.prevent="togglePanel" v-else>
                    <i class="bcs-icon bcs-icon-angle-left"></i>
                </button>
                <strong class="var-panel-title" v-show="isVarPanelShow">{{$t('可用变量')}}<span class="f12">（{{$t('模板集中引入方式')}}：{{varUserWay}}）</span></strong>
            </div>
            <div class="var-panel-list" v-show="isVarPanelShow">
                <!-- <bk-table
                    :border="true"
                    :out-border="false"
                    :data="varList">
                    <bk-table-column :label="$t('变量名')" :show-overflow-tooltip="false" min-width="200">
                        <template slot-scope="props">
                            <bcs-popover :content="props.row.name" placement="right">
                                <span class="var-name">{{props.row.name}}</span>
                            </bcs-popover>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="$t('KEY')" :show-overflow-tooltip="true" min-width="200">
                        <template slot-scope="props">
                            <bcs-popover :content="props.row.key" placement="right">
                                <span class="var-key">{{props.row.key}}</span>
                            </bcs-popover>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="$t('操作')" :show-overflow-tooltip="true">
                        <template slot-scope="props">
                            <bk-button class="var-copy-btn" :data-clipboard-text="`{{${props.row.key}}}`" type="default">
                                <i class="bcs-icon bcs-icon-clipboard"></i>
                            </bk-button>
                        </template>
                    </bk-table-column>
                </bk-table> -->
                <table class="bk-table biz-var-table">
                    <thead>
                        <tr>
                            <th>{{$t('变量名')}}</th>
                            <th style="width: 230px;">KEY</th>
                            <th style="width: 60px;"></th>
                        </tr>
                    </thead>
                </table>
                <div class="var-list">
                    <table class="bk-table biz-var-table">
                        <tbody>
                            <template v-if="varList.length">
                                <tr v-for="item of varList" :key="item.name">
                                    <td>
                                        <bcs-popover :content="item.name" placement="right">
                                            <span class="var-name">{{item.name}}</span>
                                        </bcs-popover>
                                    </td>
                                    <td style="width: 230px;">
                                        <bcs-popover :content="item.key" placement="right">
                                            <span class="var-key">{{item.key}}</span>
                                        </bcs-popover>
                                    </td>
                                    <td style="width: 60px;">
                                        <button class="var-copy-btn m5" :data-clipboard-text="`{{${item.key}}}`" type="default">
                                            <i class="bcs-icon bcs-icon-clipboard"></i>
                                        </button>
                                    </td>
                                </tr>
                            </template>
                            <template v-else>
                                <tr>
                                    <td colspan="3">
                                        <bcs-exception type="empty" scene="part"></bcs-exception>
                                    </td>
                                </tr>
                            </template>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import Clipboard from 'clipboard'
    import clickoutside from '@/directives/clickoutside'
    import { catchErrorHandler } from '@open/common/util'

    export default {
        directives: {
            clickoutside
        },
        data () {
            return {
                activeRoute: this.$route.name,
                varUserWay: `{{${this.$t('变量')}KEY}}`,
                isVarPanelShow: false,
                runEnv: window.RUN_ENV
            }
        },
        computed: {
            varList () {
                return this.$store.state.variable.varList
            },
            deployments () {
                const deployments = this.$store.state.k8sTemplate.deployments
                if (this.isVersionIsDraf) {
                    return deployments
                } else {
                    return deployments.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            services () {
                const services = this.$store.state.k8sTemplate.services
                if (this.isVersionIsDraf) {
                    return services
                } else {
                    return services.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            configmaps () {
                const configmaps = this.$store.state.k8sTemplate.configmaps
                if (this.isVersionIsDraf) {
                    return configmaps
                } else {
                    return configmaps.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            secrets () {
                const secrets = this.$store.state.k8sTemplate.secrets
                if (this.isVersionIsDraf) {
                    return secrets
                } else {
                    return secrets.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            daemonsets () {
                const daemonsets = this.$store.state.k8sTemplate.daemonsets
                if (this.isVersionIsDraf) {
                    return daemonsets
                } else {
                    return daemonsets.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            jobs () {
                const jobs = this.$store.state.k8sTemplate.jobs
                if (this.isVersionIsDraf) {
                    return jobs
                } else {
                    return jobs.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            ingresss () {
                const ingresss = this.$store.state.k8sTemplate.ingresss
                if (this.isVersionIsDraf) {
                    return ingresss
                } else {
                    return ingresss.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            HPAs () {
                const HPAs = this.$store.state.k8sTemplate.HPAs
                if (this.isVersionIsDraf) {
                    return HPAs
                } else {
                    return HPAs.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            statefulsets () {
                const statefulsets = this.$store.state.k8sTemplate.statefulsets
                if (this.isVersionIsDraf) {
                    return statefulsets
                } else {
                    return statefulsets.filter(item => {
                        // 过滤出没保存在服务端的数据
                        return (item.id + '').indexOf('local_') < 0
                    })
                }
            },
            curShowVersionId () {
                return false
            },
            isVersionIsDraf () {
                if (this.curShowVersionId === '-1' || this.curShowVersionId === -1 || this.curShowVersionId === 0 || this.curShowVersionId === '0') {
                    return true
                } else {
                    return false
                }
            },
            templateId () {
                return this.$route.params.templateId
            },
            projectId () {
                return this.$route.params.projectId
            },
            projectCode () {
                return this.$route.params.projectCode
            },
            routerName () {
                return this.$route.name
            }
        },
        watch: {
            varList () {
                this.clipboardInstance = new Clipboard('.var-copy-btn')
                this.clipboardInstance.on('success', e => {
                    this.$bkMessage({
                        theme: 'success',
                        message: this.$t('复制成功')
                    })
                    this.isVarPanelShow = false
                })
            },
            routerName (val) {
                this.activeRoute = val
            }
        },
        mounted () {
            this.initVarList()
        },
        beforeDestroy () {
            if (this.clipboardInstance && this.clipboardInstance.off) {
                this.clipboardInstance.off('success')
            }
        },
        methods: {
            /**
             * 展示/隐藏变量面板
             */
            togglePanel () {
                this.isVarPanelShow = !this.isVarPanelShow
            },

            hidePanel () {
                this.isVarPanelShow = false
            },

            /**
             * 切换到相应的模板集资源
             * @param  {string} target 资源名
             */
            toggleRouter (target) {
                if (this.clipboardInstance && this.clipboardInstance.off) {
                    this.clipboardInstance.off('success')
                }
                if (this.routerName === target) {
                    return false
                } else {
                    const from = this.routerName
                    this.$emit('tab-change', from, target)
                }
            },

            goResource (target) {
                this.activeRoute = target

                this.$router.push({
                    name: target,
                    params: {
                        projectId: this.projectId,
                        projectCode: this.projectCode,
                        templateId: this.templateId
                    }
                })
            },

            /**
             * 初始化变量列表
             */
            async initVarList () {
                const projectId = this.projectId

                try {
                    await this.$store.dispatch('variable/getBaseVarList', projectId)
                } catch (e) {
                    catchErrorHandler(e, this)
                }
            }
        }
    }

</script>
<style scoped lang="postcss">
    @import '@/css/variable.css';
    @import '@/css/mixins/ellipsis.css';
    @import '@/css/mixins/scroller.css';

    .biz-var-panel {
        width: 495px;
        position: absolute;
        right: -473px;
        top: 0;
        bottom: 0;
        z-index: 1000;
        transition: right ease 0.3s;

        .var-panel-header {
            height: 60px;
            line-height: 60px;
            background: rgba(250, 251, 253, 1);
            border-bottom: 1px solid #DDE4EB;
        }

        &.show {
            right: 0;
            border-left: 1px solid #DDE4EB;
            background: #fff;
            box-shadow: -3px 0 10px rgba(0, 0, 0, .05);

            .var-panel-trigger {
                left: -1px;
                transform: rotate(-180deg);
            }

            .var-panel-title {
                opacity: 1;
            }
        }
    }

    .var-panel-trigger {
        height: 59px;
        width: 24px;
        font-size: 14px;
        background: #fff;
        border: none;
        position: relative;
        left: -1px;
        border-left: 1px solid #DDE4EB;
        border-right: 1px solid #DDE4EB;
        transition: transform ease 0.3s;

        .bcs-icon {
            margin-left: -3px;
        }
    }

    .var-panel-title {
        height: 60px;
        line-height: 60px;
        font-size: 16px;
        color: #737987;
        padding-left: 10px;
        opacity: 0;
    }

    .var-list {
        overflow: auto;
        position: absolute;
        top: 120px;
        bottom: 0;
        width: 100%;
        border-top: 1px solid #DDE4EB;
        @mixin scroller;

        .var-name {
            vertical-align: middle;
            max-width: 170px;
            @mixin ellipsis;
        }

        .var-key {
            vertical-align: middle;
            max-width: 185px;
            @mixin ellipsis;
        }

        .biz-var-table {
            margin-top: -1px;
        }
    }

    .biz-var-table>thead>tr>th {
        background: rgba(250, 251, 253, 1);
    }

    .biz-var-table>tbody>tr>td {
        border: 1px solid #eee;

        &:first-child {
            border-left: none;
        }

        &:last-child {
            border-right: none;
        }
    }

    .biz-var-table>thead>tr>th,
    .biz-var-table>thead>tr>td,
    .biz-var-table>tbody>tr>th,
    .biz-var-table>tbody>tr>td {
        height: 43px;
        padding: 0 20px;

        &:last-child {
            padding: 0;
        }
    }

    .var-copy-btn {
        width: 43px;
        height: 43px;
        text-align: center;
        line-height: 43px;
        background: #fff;
        border: none;

        &:hover {
            color: #3C96F5;
            background: rgba(235, 244, 255, 1);
            box-shadow: 0 0 1px #ABD4FF;
        }
    }

    .empty-message {
        text-align: center;
        padding: 20px;
    }

</style>
