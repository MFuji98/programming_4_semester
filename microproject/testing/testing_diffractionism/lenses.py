import diffractsim
diffractsim.set_backend("CUDA") #Change the string to "CUDA" to use GPU acceleration

from diffractsim import PolychromaticField, Lens, ApertureFromImage, cf, nm, mm, cm, CircularAperture

F = PolychromaticField(
    spectrum = 4*cf.illuminant_d65, 
    extent_x=15. * mm, extent_y=15. * mm, 
    Nx=1500, Ny=1500,
)

F.add(ApertureFromImage(".png", image_size=(4. * mm, 4. * mm), simulation = F))

# F.add(Lens(f = 1000*cm, radius = 10*cm, aberration = lambda x,y: 1/(2*10*cm) * (x**2+y**2)))
# F.add(Lens(f = 1000*cm))
F.propagate(z=10*cm)

rgb =F.get_colors()
F.plot_colors(rgb, xlim=[-1.5* mm, 1.5* mm], ylim=[0* mm, 1.8* mm])