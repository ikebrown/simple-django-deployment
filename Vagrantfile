Vagrant::Config.run do |config|
    config.vm.define :develop do |config|
      config.vm.box = "lucid32"
      config.vm.network :hostonly, "33.33.33.10"
      config.vm.customize ["modifyvm", :id, "--memory", "256"]
    end
end
