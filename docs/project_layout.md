# Epiphany Project Layout

## Folders

### .gitlab

The `.gitlab` folder is of course, specific to GitLab. It provides several templates used by GitLab to aid in tracking issues and merge requests (a.k.a. pull requests). This folder should only be modified by the project owner since it only deals with workflow so you most likely will never have a need to work with it.

### architecture

The `architecture` folder is a very important. It contains everything needed to understand what Epiphany is from an Architectural point of view. The Architectural documentation can be found [here](/architecture/docs/index.md) along with the specifics for the folders in /architecture.

### assets

The `assets` folder contains all of the assets used including logos and presentations slides. You should place all of your images in the `images` folder and any specific sub-folder that you feel will help keep things more organized. Also, the `slides` folder holds PowerPoint slides of Epiphany. `Epiphany.pptx` This is a single presentation that contains chapters (sections) along with navigation so that you can use a single presentation to address different audiences. Some of the sections repeat themselves in different ways because of the design so keep that in mind.

### bin

The `bin` folder is used to hold executable files such as binaries, scripts etc. This folder should *only* hold items required by Epiphany as a dependency and that is not part of a full project. For example, the `template_engine` executable script handles all of the template features for Epiphany and it's small in size. If you need to include a project like dependency then you would add the package information in the `dependencies` section of the primary Epiphany data file. This dependency would then be pulled down during the pre-build process from where ever you point it to. So, small executable scripts or binaries that are not part of a larger package should be considered to go here. If in doubt then make it a dependency instead.

### build

The `build` folder is what it says - it holds the build.

## Critical Folder

### core

The `core` folder holds the core of Epiphany.

### data

The `data` folder holds all of the yaml data files. This folder is what is most updated by application developers for their own product needs. Epiphany is fully data driven so making changes here will build out a new version of Epiphany and/or your product (maybe).

### core-extensions

The `core-extensions` folder holds additional (extensions) items that could be promoted to `core` but instead is placed here first.

### examples

The `examples` folder holds a number of examples of how to use Epiphany.

### extras

The `extras` folder contains additional (extra) goodies that may help in your workflow etc. This includes editor examples and more.
