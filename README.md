# Toybrick.md

## 功能

1. Markdown内预置若干令牌，通过令牌来划分不同层次和“块”，通过对块的替换而实现生成。整个页面，只需```gen()```
2. 提供原生i18n支持，不同语言无需反复deploy，只要适时订正对应语言文档。API亦可矩阵式生成。
3. 提供两种模板：**可序表格**与**API库**
4. 支持带参启动来决定进入配置器还是构建器，允许本地手工运行或GH Action
5. 预置多个常用模块，如CI badge等，无需手写，只需在json内指定内容和显示位置，自动为你添加，堪比```README.rst```

## 技术细节

1. column定义行列，并在构建前对data进行检查
2. 所有table理论上都是sortable的

## 来源

本项目受如下项目的启发而构建：
+ osmlab/name-suggestion-index
+ LaoshuBaby/china-university-thesis-index
+ Uni-Gal/UniGal-EnforcementProposal

## 可能会有用的其他项目

如果您觉得本项目不太实用，可以参考下面这些项目

他们或许会有相似的功能，且经过了社区的考验。

+ docsifyjs/docsify
+ ap0llo/mddocs
+ mendersoftware/mender-docs
+ jedelman8/ansible-webdocs
+ raghakot/markdown-apidocs