Vagrant::Config.run do |config|
  config.vm.define :develop do |config|
    config.vm.box = "lucid32"
    config.vm.forward_port 22, 2222
    config.vm.forward_port 80, 8080
    config.vm.network :bridged
    config.vm.customize ["modifyvm", :id, "--memory", "256"]
    Vagrant::Config.run do |config|
      config.vm.provision :shell, :path => "do_provision.sh"
    end
  end
end
