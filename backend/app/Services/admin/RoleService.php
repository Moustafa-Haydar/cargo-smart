<?php
namespace App\Services\Admin;
use App\Models\Role;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use App\Http\Requests\StoreUserRequest;

class RoleService
{
    public static function addRole(Request $request)
    {
        $data = $request->validated();
        $role = Role::create($data);
        return ($role);
    }

    public static function getAllRoles($id = null)
    {
        if ($id == null) {
            return Role::all();
        }
        return Role::find($id);
    }

    public static function deleteAllRoles($id = null)
    {
        if ($id == null) {
            // delete all roles
            return Role::truncate();
        }

        $role = Role::find($id);
        if (!$role) {
            // role not found
            return false;
        }

        // Delete the role with the given ID
        return $role->delete();
    }

}