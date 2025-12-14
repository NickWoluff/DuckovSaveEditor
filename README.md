# 鸭科夫存档编辑器 (Duckov Save Editor)
[![Downloads](https://img.shields.io/github/downloads/NickWoluff/DuckovSaveEditor/total?style=flat-square&logo=github)](https://github.com/NickWoluff/DuckovSaveEditor/releases)[![Last Version](https://img.shields.io/github/release/NickWoluff/DuckovSaveEditor/all.svg?style=flat-square)](https://github.com/NickWoluff/DuckovSaveEditor/releases)
## 简介

**鸭科夫存档编辑器** 是一款专为《逃离鸭科夫》（《Escape from Duckov》）游戏设计的存档编辑工具，方便玩家查看和修改背包及仓库中的物品属性。
 支持查看物品数量、耐久度等信息，并方便快捷地修改存档数据。

> 作者：尼克狼唔 `Nick Woluff`<img src="assets/icon.ico" width="16" height="16" />

## 功能特点

- **查看存档内容**：支持背包和仓库的物品信息显示
- **编辑物品属性**：可修改数量、耐久、磨损等
- **自动备份**：保存时自动生成 `.backup` 文件
- **图形 UI**：简单直观的图形界面
- 更多功能持续更新中

## 系统要求

- **操作系统**：Windows 10 / 11
- **无需安装 Python，双击 exe 文件即可直接运行**

## 使用说明

  1. 前往[Releases页面](https://github.com/NickWoluff/DuckovSaveEditor/releases)下载最新版本 `DuckovSaveEditor.exe`
2. 双击运行程序
3. 点击 **“选择存档文件”**（默认路径为 `C:\Users\<用户名>\AppData\LocalLow\TeamSoda\Duckov\Saves`）
4. 浏览物品列表
5. 双击物品可修改允许修改的属性，包括但不限于物品数量、耐久度等
6. 点击 **“应用全部修改”** 保存修改

注意：
> 单格修改数量请勿超过该物品最大堆叠数量，避免存档数据丢失或损坏。建议搭配[《更多最大堆叠数量》](https://steamcommunity.com/sharedfiles/filedetails/?id=3588401047)mod使用；
> 程序会在同目录生成 `.backup` 文件防止存档丢失，若出现修改后无法进入游戏等异常情况，可使用 `.backup` 文件恢复修改前的最新存档，无须退回旧存档。


## 发布说明

- 仅用于学习用途免费分享，勿用于商业分发
- 若需反馈问题或建议，请在 Issues 中留言

## 版权信息

```
© 2025 Nick Woluff  All rights reserved.
```
